from datetime import datetime, timedelta
from itertools import combinations, product
from typing import Union

import swisseph as swe

from py_astrolab import KrInstance


class Transits():
    def __init__(self, 
            user: KrInstance, 
            start: datetime, 
            end: datetime,
            settings: Union[str, None] = None):
        self.user = user
        self.start = start
        self.end = end
        self.settings = settings
        self.natal_aspects_changes = {}
        self.transit_aspects_changes = {}
        self.previous_natal_aspects = None
        self.previous_transit_aspects = None

        self.planets = range(swe.SUN, swe.SATURN)
        self.aspects = [0, 30, 60, 90, 120, 150, 180]
        self.planet_names = {
            swe.SUN: {'name': 'Sun', 'orbit': 3, 'interval': timedelta(minutes=5)}, # 6 giorni in aspetto
            # 365 giorni / 360 gradi = 1 giorni per grado
            # 3 gradi di orbita * 2 * 1 giorni = 6 giorni in aspetto
            swe.MOON: {'name': 'Moon','orbit': 1, 'interval': timedelta(minutes=5)}, # 3,6 ore in aspetto
            # 27.3 giorni / 360 gradi = 1 ora e 49 minuti per grado (109 minuti)
            # 1 gradi di orbita * 2 * 1 ora e 49 minuti = 3,6 ore
            swe.MERCURY: {'name': 'Mercury','orbit': 3, 'interval': timedelta(hours=1)}, # 1,5 giorni in aspetto
            # 88 giorni / 360 gradi = 5,9 ore per grado (351 minuti)
            # 3 gradi di orbita * 2 * 5,9 ore = 1,5 giorni
            swe.VENUS: {'name': 'Venus','orbit': 3, 'interval': timedelta(hours=1)}, # 3,75 giorni in aspetto
            # 225 giorni / 360 gradi = 15 ore per grado
            # 3 gradi di orbita * 2 * 15 ore = 3,75 giorni
            swe.MARS: {'name': 'Mars','orbit': 5, 'interval': timedelta(hours=1)}, # 20 giorni
            # 687 giorni / 360 gradi = 1.9 giorni per grado (45,6 ore)
            # 5 gradi di orbita * 2 * 1.9 giorni = 20 giorni
            swe.JUPITER: {'name': 'Jupiter','orbit': 5, 'interval': timedelta(hours=1)}, # 4 mesi in aspetto
            # (11.86 anni * 365.25 giorni/anno) / 360 gradi = 12 giorni per grado
            # 5 gradi di orbita * 2 * 12 giorni = 120 giorni (4 mesi)
            swe.SATURN: {'name': 'Saturn','orbit': 5, 'interval': timedelta(days=1)} # 10 mesi
            # (29.5 anni * 365.25 giorni/anno) / 360 gradi = 30 giorni per grado
            # 5 gradi di orbita * 2 * 30 giorni = 300 giorni (10 mesi)
        }
        self.aspect_names = {
            0: 'conjunction',
            30: 'semi-sextile',
            60: 'sextile',
            90: 'square',
            120: 'trine',
            150: 'quincunx',
            180: 'opposition',
        }
        self.julday_cache = dict()
        self.long_cache = dict()
        self.times, self.positions = self.calculate_positions()
        self.orb_cache = dict()
    
    def calc_long(self, jd, planet):
        cache_tuple = (jd, planet)
        if cache_tuple in self.long_cache:
            return self.long_cache[cache_tuple]
        long = swe.calc(jd, planet)[0][0]
        self.long_cache[cache_tuple] = long
        return long

    def calc_orb(self, jd, planet1, planet2, aspect, natal_planet_orb=None):
        cache_tuple = (jd, planet1, planet2, aspect)
        if cache_tuple in self.orb_cache:
            return self.orb_cache[cache_tuple]
        lon1 = self.calc_long(jd, planet1)
        lon2 = self.calc_long(jd, planet2) if not natal_planet_orb else natal_planet_orb
        angle = self.angle_difference(lon1, lon2)
        orb = abs(abs(angle) - aspect)
        self.orb_cache[cache_tuple] = orb
        return orb

    def find_aspects(self, look_for_planets, waxing_only, waning_only):
        look_for_planets = set(self.planet_names.keys()) if look_for_planets is None else look_for_planets
        natal_positions = {planet_data['name']: planet_data['abs_pos'] for planet_data in self.user.planets_list}
        aspects = self.__find_aspects(self.times, self.positions, natal_positions, look_for_planets, waxing_only, waning_only)
        return aspects

    def angle_difference(self, angle1, angle2):
        return 180 - abs(abs(angle1 - angle2) - 180)

    def jd_to_datetime(self, jd):
        if jd in self.julday_cache:
            return self.julday_cache[jd]
        jd = jd + 0.5
        Z = int(jd)
        F = jd - Z
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4.)
        B = A + 1524
        C = int((B - 122.1) / 365.25)
        D = int(365.25 * C)
        E = int((B - D) / 30.6001)
        day = B - D - int(30.6001 * E) + F
        month = E - 1 if E < 14 else E - 13
        year = C - 4716 if month > 2 else C - 4715
        day, fractional_day = divmod(day, 1)
        hour, fractional_hour = divmod(fractional_day * 24, 1)
        minute, _ = divmod(fractional_hour * 60, 1)
        minute = round(minute)
        dt = datetime(int(year), int(month), int(day), int(hour), int(minute))
        self.julday_cache[jd] = dt
        return dt
    
    def datetime_to_jd(self, dt: datetime):
        if dt in self.julday_cache:
            return self.julday_cache[dt]
        julday = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60)
        self.julday_cache[dt] = julday
        return julday

    def binary_search(self, time1, time2, planet1, planet2, aspect, target_orb, natal_planet_orb):
        jd1 = self.datetime_to_jd(time1)
        jd2 = self.datetime_to_jd(time2)
        while jd2 - jd1 > 6.94e-4:  # 1 minuto in giorni.
            jd = jd1 + (jd2 - jd1) / 2
            orb = self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb)  # Calcola l'orbita
            if abs(orb - target_orb) < 0.1:  # Se l'orbita è vicina a target_orb
                jd = round(jd * 1440) / 1440  # Arrotonda al minuto più vicino
                return self.jd_to_datetime(jd), orb
            if orb > target_orb:
                jd2 = jd
            else:
                jd1 = jd
        jd1 = round(jd1 * 1440) / 1440  # Arrotonda al minuto più vicino
        orb = self.calc_orb(jd1, planet1, planet2, aspect, natal_planet_orb)  # Calcola l'orbita
        return self.jd_to_datetime(jd1), orb

    def backward_binary_search(self, planet1, planet2, aspect, orbit_tolerance, natal_planet_orb, interval):
        # Prima, determina se l'aspetto è presente all'inizio.
        # interval = min(self.planet_names[planet1]['interval'], self.planet_names[planet2]['interval'])
        current_time = self.start
        jd = self.datetime_to_jd(current_time)
        angle_current_time = self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb)
        # Se l'aspetto è presente all'inizio, trova il giorno in cui l'aspetto non è presente.
        if angle_current_time <= orbit_tolerance:
            while True:  # Loop finché l'aspetto è presente
                current_time -= interval  # Vai indietro di un intervallo di tempo
                jd = self.datetime_to_jd(current_time)
                angle_current_time = self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb)
                if angle_current_time > orbit_tolerance:  # Se l'aspetto non è presente, esci dal loop
                    break
            # Ora abbiamo il tempo in cui l'aspetto non era presente, cerchiamo il minuto esatto nell'intervallo di tempo successivo.
            lower_bound = current_time + interval  # L'inizio dell'intervallo successivo
            upper_bound = lower_bound + interval
        # Se l'aspetto non è presente all'inizio, trova il giorno in cui l'aspetto è presente.
        else:
            while True:  # Loop finché l'aspetto non è presente
                jd = self.datetime_to_jd(current_time)
                angle_current_time = self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb)
                if angle_current_time <= (orbit_tolerance + 0.1):  # Se l'aspetto è presente, esci dal loop
                    break
                current_time -= interval  # Vai indietro di un intervallo di tempo
            # Ora abbiamo il tempo in cui l'aspetto era presente per la prima volta, cerchiamo il minuto esatto nell'intervallo di tempo precedente.
            upper_bound = current_time  # La fine dell'intervallo precedente
            lower_bound = upper_bound - interval
        # Ora utilizza binary_search tra lower_bound e upper_bound
        return self.binary_search(lower_bound, upper_bound, planet1, planet2, aspect, orbit_tolerance, natal_planet_orb)

    def forward_binary_search(self, planet1, planet2, aspect, target_orb, current_time, natal_planet_orb, interval):
        # interval = min(self.planet_names[planet1]['interval'], self.planet_names[planet2]['interval'])
        while True:
            jd = self.datetime_to_jd(current_time)
            angle_current_time = self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb)
            if angle_current_time > target_orb + 0.1:
                break
            current_time += interval
        upper_bound = current_time
        lower_bound = current_time - interval
        return self.binary_search(lower_bound, upper_bound, planet1, planet2, aspect, target_orb, natal_planet_orb)

    def calculate_positions(self):
        minutes_diff = int((self.end - self.start).total_seconds() / 60)
        times = [self.start + timedelta(minutes=i) for i in range(0, minutes_diff, 5)]
        positions = {planet: [] for planet in self.planets}
        for time in times:
            jd = self.datetime_to_jd(time)
            for planet in self.planets:
                lon = self.calc_long(jd, planet)
                positions[planet].append(lon)
        return times, positions

    def __find_aspects(self, times, positions, natal_positions, look_for_planets, waxing_only, waning_only):
        aspect_list = [] 
        current_aspects = set()
        for planet1, planet2 in product(self.planets, natal_positions.keys()):
            if planet1 not in look_for_planets:
                continue
            planet2_number = next((planet for planet, info in self.planet_names.items() if info['name'] == planet2), None)
            if planet2_number is None:
                continue
            interval = self.planet_names[planet1]['interval']
            orbit_tolerance = self.planet_names[planet1]['orbit']
            natal_position = natal_positions[planet2]
            for time1, time2, lon1_1, lon1_2 in zip(times, times[1:], positions[planet1], positions[planet1][1:]):
                for a in self.aspects:
                    p1_name = self.planet_names[planet1]['name']
                    p2_name = planet2
                    aspect_name = self.aspect_names[a]
                    aspect_tuple = (p1_name, p2_name, aspect_name)
                    diff1 = self.angle_difference(lon1_1, natal_position)
                    diff2 = self.angle_difference(lon1_2, natal_position)
                    if not ((diff1 - a) * (diff2 - a) <= 0) and not (abs(diff1 - a) <= orbit_tolerance) and not (abs(diff2 - a) <= orbit_tolerance):
                        current_aspects.discard((self.planet_names[planet1]['name'], planet2, self.aspect_names[a]))
                        continue
                    aspect_tuple = (self.planet_names[planet1]['name'], planet2, self.aspect_names[a])
                    if aspect_tuple in current_aspects:
                        continue
                    start_time, start_orb = None, None
                    if time1 == self.start and not waxing_only and not waning_only:
                        start_time, start_orb = self.backward_binary_search(planet1, planet2_number, a, orbit_tolerance, natal_position, interval)
                    elif not waning_only:
                        start_time, start_orb = self.binary_search(time1, time2, planet1, planet2_number, a, orbit_tolerance, natal_position)
                        if waxing_only and abs(start_orb - orbit_tolerance) >= 0.1:
                            start_time = None
                    finish_time = None if waxing_only or waning_only else self.forward_binary_search(planet1, planet2_number, a, orbit_tolerance, start_time, natal_position, interval)[0]
                    exact_time, exact_orb = (self.binary_search(self.start, self.end, planet1, planet2_number, a, 0, natal_position) if waning_only else (None, None))
                    if waning_only and exact_orb >= 0.1:
                        exact_time = None
                    if start_time or exact_time:
                        if start_time:
                            p1_long = self.calc_long(self.datetime_to_jd(start_time), planet1)
                            duration = finish_time-start_time if finish_time is not None else None
                        elif exact_time:
                            p1_long = self.calc_long(self.datetime_to_jd(exact_time), planet1)
                            duration = None
                        p1_sign = self.get_zodiac_sign(p1_long)
                        p2_sign = getattr(self.user, p2_name.lower())['signs'][0]
                        p1_house = self.point_in_house(p1_long)
                        p2_house = getattr(self.user, p2_name.lower())['house']   
                        aspect_dict = {
                            'p1_name': p1_name,
                            'p2_name': p2_name,
                            'p1_sign': p1_sign,
                            'p2_sign': p2_sign,
                            'p1_house': p1_house,
                            'p2_house': p2_house,
                            'aspect': aspect_name,
                            'start': start_time,
                            'exact': exact_time,
                            'finish': finish_time,
                            'duration': duration,
                            'start_orb': start_orb,
                            'exact_orb': exact_orb
                        }
                        if waning_only:
                            if exact_time:
                                aspect_list.append(aspect_dict)
                        else:
                            aspect_list.append(aspect_dict)
                    current_aspects.add(aspect_tuple)
        aspect_list.sort(key=lambda x: x['start'] if x['start'] else x['exact'])
        return aspect_list

    def get_zodiac_sign(self, lon):
        signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 
                'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']
        return signs[int(lon // 30)]

    def calculate_transitions(self):
        sign_transitions = dict()
        house_transitions = dict()
        direction_transitions = dict()
        for planet in self.planet_names:
            current_time = self.start
            while current_time <= self.end:
                jd = self.datetime_to_jd(current_time)
                lon = self.calc_long(jd, planet)
                current_sign = self.get_zodiac_sign(lon)
                current_house = self.point_in_house(lon)
                current_direction = swe.calc(jd, planet)[0][3] < 0
                interval = timedelta(minutes=15)
                while current_time <= self.end:
                    current_time += interval
                    jd = self.datetime_to_jd(current_time)
                    lon = self.calc_long(jd, planet)
                    old_sign = current_sign
                    old_house = current_house
                    old_direction = current_direction
                    current_sign = self.get_zodiac_sign(lon)
                    current_house = self.point_in_house(lon)
                    current_direction = swe.calc(jd, planet)[0][3] < 0
                    if old_sign != current_sign:
                        sign_transitions[self.planet_names[planet]['name']] = {'when': current_time, 'old': old_sign, 'new': current_sign}
                    if old_direction != current_direction:
                        direction_status = "retrograde" if current_direction else "direct"
                        direction_transitions[self.planet_names[planet]['name']] = {'when': current_time, 'status': direction_status}
                    if old_house != current_house:
                        house_transitions[self.planet_names[planet]['name']] = {'when': current_time, 'old': old_house, 'new': current_house}
        return sign_transitions, house_transitions, direction_transitions

    def new_moon(self):
        new_moon_obj = dict()
        new_moon_obj['when'], new_moon_obj['orb'] = self.backward_binary_search(0, 1, 0, 0, None, timedelta(minutes=30))
        new_moon_long = self.calc_long(self.datetime_to_jd(new_moon_obj['when']), 1)
        sign = self.get_zodiac_sign(new_moon_long)
        new_moon_obj['sign'] = sign
        new_moon_obj['house'] = self.point_in_house(new_moon_long)
        return new_moon_obj

    def lunar_phase(self):
        jd = self.datetime_to_jd(self.start)
        moon_longitude = self.calc_long(jd, swe.MOON)
        sun_longitude = self.calc_long(jd, swe.SUN)
        phase_angle = self.angle_difference(moon_longitude, sun_longitude)
        if phase_angle < 0:
            phase_angle += 360
        if phase_angle < 11.25 or phase_angle >= 348.75:
            phase_name = "New Moon"
        elif phase_angle < 78.75:
            phase_name = "Waxing Crescent"
        elif phase_angle < 101.25:
            phase_name = "First Quarter"
        elif phase_angle < 168.75:
            phase_name = "Waxing Gibbous"
        elif phase_angle < 191.25:
            phase_name = "Full Moon"
        elif phase_angle < 258.75:
            phase_name = "Waning Gibbous"
        elif phase_angle < 281.25:
            phase_name = "Last Quarter"
        else:
            phase_name = "Waning Crescent"
        output = {
            'phase': phase_name,
            'sign': self.get_zodiac_sign(moon_longitude),
            'house': self.point_in_house(moon_longitude)
        }
        return output

    def point_in_house(self, point_long):
        for house in self.user.houses_list:
            lower_bound = house['abs_pos']
            upper_bound = house['abs_pos'] + 30
            if lower_bound <= point_long < upper_bound:
                return house['name']