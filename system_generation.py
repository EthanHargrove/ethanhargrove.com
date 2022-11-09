import rebound
import numpy as np


#Using the Kroupa initial mass function to generate stellar mass probabilities
def get_star_probs(num):
    brackets = np.geomspace(0.08, 2.22, num=num, endpoint=True)
    coeff = (-(7**1.3)/(30*(10**0.6)*(0.5**0.3))) - (-(7**1.3)/(30*(10**0.6)*(0.08**0.3))) + (-(7**1.3)/(260*(10**0.6)*(2.22**1.3))) - (-(7**1.3)/(260*(10**0.6)*(0.5**1.3)))
    star_probs = np.zeros(len(brackets)-1)

    for i, lower in enumerate(brackets[:-1]):
        upper = brackets[i+1]
        if (lower < 0.5) and (upper <= 0.5):
            star_probs[i] = (-(7**1.3)/(30*(10**0.6)*(upper**0.3))) - (-(7**1.3)/(30*(10**0.6)*(lower**0.3)))
        elif (lower < 0.5) and (upper >= 0.5):
            star_probs[i] = (-(7**1.3)/(30*(10**0.6)*(0.5**0.3))) - (-(7**1.3)/(30*(10**0.6)*(lower**0.3))) + (-(7**1.3)/(260*(10**0.6)*(upper**1.3))) - (-(7**1.3)/(260*(10**0.6)*(0.5**1.3)))
        else:
            star_probs[i] = (-(7**1.3)/(260*(10**0.6)*(upper**1.3))) - (-(7**1.3)/(260*(10**0.6)*(lower**1.3)))

    star_probs /= coeff
    return brackets, star_probs


#Randomly generating star mass using the stellar mass probabilities
def get_star_mass(num=1000, brackets=None, star_probs=None):
    if (brackets is None) or (star_probs is None):
        brackets, star_probs = get_star_probs(num)
    mass_ind = np.random.choice(num-1, 1, p=star_probs)
    lower = brackets[mass_ind]
    upper = brackets[mass_ind+1]
    star_mass = np.random.uniform(lower,upper)[0]

    return star_mass


#Degree to radian converter
def deg_to_rad(deg_inc):
    deg_sep = 90 - deg_inc
    rad_inc = deg_sep * (np.pi/180)

    return rad_inc


#Randomly generate inclination given period
def get_inclination(period):
    if 4 <= period <= 9:
        mini = 21.8604 + 23.05143*period - 2.848991*period**2 + 0.1174863*period**3
        mini *= np.random.uniform(0.98,1.02)
    if 7 <= period < 26:
        epsi = (98/100)*(99/101)
        inc = np.random.f(100,99) * (89.9 / epsi)
        diff = inc - 89.9
        plusminus = np.random.rand()
        maxi = 88.5 + plusminus * 1.6
        if (period < 4) or (period > 9):
            mini = 90 - plusminus * 6
        if diff < 0:
            inc -= 1.25 * np.random.rand() * diff
            inc = min(maxi, inc)
            inc = max(mini, inc)
        else:
            inc = max(mini, inc)
            inc = min(maxi, inc)

        if plusminus > 0.9975:
            inc += 6 * np.random.rand()

        elif plusminus < 0.0002:
            inc = np.random.uniform(80,90.1)
            inc = 2.970297*inc - 187.6238
    if 2 <= period < 7:
        inc = np.random.uniform(79,91)
        inc = inc + np.random.rand()*np.random.rand() - np.random.rand()*np.random.rand()
        diff = inc - 88
        plusminus = np.random.rand()
        maxi = 88 + plusminus * 2.1
        if (period < 4) or (period > 9):
            mini = 82 - plusminus * 2
        inc = max(mini, inc)
        inc = min(maxi, inc)

        if plusminus > 0.9995:
            inc += 11 * np.random.rand()

        elif plusminus < 0.002:
            inc = np.random.uniform(80,90.1)
            inc = 2.970297*inc - 187.6238


    elif period < 2:
        inc = np.random.uniform(77.5,90.1)
        plusminus = np.random.rand()
        maxi = 87 + plusminus * 3.1
        mini = 80 - plusminus * 2.5
        inc = min(maxi,inc)
        inc = max(mini,inc)

    elif 26 <= period < 600:
        inc = np.random.uniform(84,90)
        diff = abs(inc - 88)
        plusminus = np.random.rand()
        maxi = 89 + plusminus * 1.1
        mini = 88 - plusminus * 2
        inc += 5 * np.random.rand() * diff
        inc = min(maxi, inc)
        inc = max(mini, inc)

        if plusminus > 0.9995:
            inc += 7 * np.random.rand()
        elif plusminus < 0.0075:
            inc = np.random.uniform(86,90)
            inc = 3.5 * inc - 255

    elif period >= 600:
        inc = np.random.uniform(88,90)
        plusminus = np.random.rand()
        if plusminus < 0.065:
            inc = 27.61905*inc - 2398.476
        inc = max(inc,46)
        if inc == 46:
            shift = np.random.rand()
            if shift <= 0.25:
                inc = np.random.uniform(46,50)
            elif 0.25 < shift <= 0.5:
                inc = np.random.uniform(50,55)
            elif 0.5 < shift <= 0.75:
                inc = np.random.uniform(55,60)
            else:
                inc = np.random.uniform(46,60)
    rad_inc = deg_to_rad(inc)

    return inc, rad_inc


#Randomly generate eccentricity given period
def get_ecc(period):
    if period < 1:
        epsi = (1/3)*(10/12)
        ecc = np.random.f(3,10) * (0.001/epsi)
        ecc = min(0.1,ecc)
    elif 1 <= period < 3:
        epsi = (1/3)*(18/20)
        ecc = np.random.f(3,18) * (0.005/epsi)
        diff = ecc - 0.005
        if diff > 0:
            ecc += 2.8 * np.random.rand() * diff
            ecc = min(0.25,ecc)
        else:
            ecc += 0.5 * np.random.rand() * diff
            ecc = max(0,ecc)
    elif 3 <= period < 11:
        epsi = (1/3)*(16/18)
        ecc = np.random.f(3,16) * (0.01/epsi)
        diff = ecc - 0.01
        if diff > 0:
            ecc += 2.8 * np.random.rand() * diff
            ecc = min(0.575,ecc)
        else:
            ecc += 0.5 * np.random.rand() * diff
            ecc = max(0,ecc)
    elif 11 <= period < 100:
        epsi = (2/4)*(37/39)
        ecc = np.random.f(4,37) * (0.05/epsi)
        diff = ecc - 0.05
        if diff > 0:
            ecc = min(0.85,ecc)
        else:
            ecc += 0.5 * np.random.rand() * diff
            ecc = max(0,ecc)
    elif 100 <= period:
        epsi = (4/6)*(70/72)
        ecc = np.random.f(6,70) * (0.1/epsi)
        diff = ecc - 0.1
        if diff > 0:
            ecc += 0.95 * np.random.rand() * diff
        ecc = min(0.9, ecc)

    return ecc


#Randomly generate terrestrial planet
def get_terrestrial():
    mass_epsi = (7/9)*(20/22)
    mass = np.random.f(9,20)*(1.43e-5/mass_epsi)
    if 9.5459e-6 <= mass <= 2.8638e-5:
        diff = mass - 1.43e-5
        mass += 0.05*diff
    elif mass > 2.8638e-5:
        diff = mass - 2.8638e-5
        move = np.random.random()
        if move <= 1/7:
            mass += 4 * diff
        elif 1/7 < move <= 2/7:
            mass += 3.25 * diff
        elif 2/7 < move <= 3/7:
            mass += 2.5 * diff
        elif 3/7 < move <= 4/7:
            mass += 1.25 * diff
        elif 4/7 < move <= 5/7:
            mass += 0.5 * diff
        elif 5/7 < move <= 6/7:
            mass += 0.125 * diff
        mass = min(3.8e-4,mass)
        if mass == 3.8e-4:
            bump = np.random.rand()
            if bump <= 0.25:
                mass /= 1 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                mass /= 2 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                mass /= 3 + np.random.rand()
            else:
                mass /= 4 + np.random.rand()
        switch = np.random.rand()
        if switch <= 0.6:
            mass = np.random.uniform(9.5459e-6,2.8638e-5)
    elif mass < 9.5459e-6:
        diff = mass - 9.5459e-6
        mass += 0.5 * diff
        mass = max(4.5e-7,mass)
        switch = np.random.rand()
        if switch <= 0.1:
            mass = np.random.uniform(9.5459e-6,2.8638e-5)
        if mass == 4.5e-7:
            bump = np.random.rand()
            if bump <= 0.25:
                mass *= 3 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                mass *= 4 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                mass *= 5 + np.random.rand()
            else:
                mass *= 6 + np.random.rand()
    jup_mass = mass * 1047.57
    if jup_mass >= 4e-2:
        target = -49.69775 + 2411.868*jup_mass - 20605.92*jup_mass**2 + 54570.11*jup_mass**3
    else:
        target = 2.965517 + 591.8719 * jup_mass + 16822.66 * jup_mass ** 2 - 566502.5 * jup_mass ** 3
    if jup_mass <= 2e-3:
        period_epsi = (36/38)*(39/41)
        period = np.random.f(38,39) * (target/period_epsi)
        diff = period - target
        if diff < 0:
            period += 2.75 * diff * np.random.rand() * np.random.rand()
            period = max(0.35,period)
        else:
            period += 9*diff * np.random.rand() * np.random.rand()
            period = min(35, period)
    elif 2e-3 < jup_mass <= 1.3e-2:
        period_epsi = (37/39)*(39/41)
        period = np.random.f(39,39) * (target/period_epsi)
        period *= 0.75
        diff = period - target
        if -target/3 < diff < target/4:
            move = np.random.rand()
            if move <= 0.125:
                period += 1.25 * diff
            elif 0.125 < move <= 0.25:
                period += 1.5 * diff
            elif 0.25 < move <= 0.375:
                period += 1.75 * diff
            elif 0.375 < move <= 0.5:
                period += 2 * diff
            elif 0.5 < move <= 0.625:
                period += 2.125 * diff
            elif 0.625 < move <= 0.75:
                period += 2.25 * diff
            elif 0.75 < move <= 0.875:
                period += 2.5 * diff
            else:
                period += 2.75 * diff
            period = max(0.35,period)
            period = min(150,period)
            randy = np.random.rand()
            if randy <= 0.05:
                period = np.random.uniform(1.5,2.5)
            elif 0.05 < randy <= 0.1:
                period = np.random.uniform(2.5,3.5)
            elif 0.1 < randy <= 0.15:
                period = np.random.uniform(3.5,4.5)
            elif 0.15 < randy <= 0.2:
                period = np.random.uniform(4.5,5.5)
            elif 0.2 < randy <= 0.25:
                period = np.random.uniform(5.5,6.5)
            elif 0.25 < randy <= 0.3:
                period = np.random.uniform(6.5,7.5)
            elif 0.3 < randy <= 0.35:
                period = np.random.uniform(7.5,8.5)
            elif 0.35 < randy <= 0.4:
                period = np.random.uniform(8.5,9.5)
            elif 0.4 < randy <= 0.45:
                period = np.random.uniform(9.5,10.5)
        elif diff < 0:
            move = np.random.rand()
            if move <= 0.1:
                period += 0.62 * diff
            elif 0.1 < move <= 0.2:
                period += 0.53 * diff
            elif 0.2 < move <= 0.3:
                period += 0.47 * diff
            elif 0.3 < move <= 0.4:
                period += 0.40 * diff
            elif 0.4 < move <= 0.5:
                period += 0.37 * diff
            elif 0.5 < move <= 0.6:
                period += 0.32 * diff
            elif 0.6 < move <= 0.7:
                period += 0.27 * diff
            elif 0.7 < move <= 0.8:
                period += 0.22 * diff
            elif 0.8 < move <= 0.9:
                period += 0.15 * diff
            period = max(0.35,period)
            if period == 0.35:
                bump = np.random.rand()
                if bump <= 0.25:
                    mass *= 1 + np.random.rand()
                elif 0.25 < bump <= 0.5:
                    mass *= 1.5 + np.random.rand()
                elif 0.5 < bump <= 0.75:
                    mass *= 2 + np.random.rand()
                else:
                    mass *= 2.5 + np.random.rand()
        else:
            move = np.random.rand()
            if move <= 0.05:
                period += 17 * diff
            elif 0.05 < move <= 0.1:
                period += 16 * diff
            elif 0.1 < move <= 0.15:
                period += 15 * diff
            elif 0.15 < move <= 0.2:
                period += 14 * diff
            elif 0.2 < move <= 0.25:
                period += 13 * diff
            elif 0.25 < move <= 0.3:
                period += 12 * diff
            elif 0.3 < move <= 0.35:
                period += 11 * diff
            elif 0.35 < move <= 0.4:
                period += 10 * diff
            elif 0.4 < move <= 0.45:
                period += 9 * diff
            elif 0.45 < move <= 0.5:
                period += 7 * diff
            elif 0.5 < move <= 0.55:
                period += 6 * diff
            elif 0.55 < move <= 0.6:
                period += 5 * diff
            elif 0.6 < move <= 0.65:
                period += 4 * diff
            elif 0.65 < move <= 0.7:
                period += 3 * diff
            elif 0.7 < move <= 0.75:
                period += 2 * diff
            elif 0.75 < move <= 0.8:
                period += 1 * diff
            elif 0.8 < move <= 0.9:
                period += 0.5 * diff
            period = min(150,period)
        if period > target:
            shift = np.random.rand()
            if shift <= 0.25:
                period *= 1
            elif 0.25 < shift <= 0.5:
                period *= 1.25
            elif 0.5 < shift <= 0.75:
                period *= 1.5
            elif shift > 0.75:
                period *= 1.75
            period = min(150,period)
        if period == 0.35:
            bump = np.random.rand()
            if bump <= 0.25:
                period *= 1 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                period *= 2 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                period *= 3 + np.random.rand()
            else:
                period *= 4 + np.random.rand()

    elif 1.3e-2 < jup_mass <= 4e-2:
        period_epsi = (27/29)*(38/40)
        period = np.random.f(29,38) * (target/period_epsi)
        diff = period - target
        if -target/3 < diff < target:
            if diff < 0:
                period += 0.9*diff
                period = max(0.8,period)
            else:
                period += 0.3*diff
                period = min(575, period)
        elif diff < 0:
            move = np.random.rand()
            if move <= 0.4:
                period += 0.62 * diff
            elif 0.4 < move <= 0.6:
                period += 0.57 * diff
            elif 0.6 < move <= 0.7:
                period += 0.47 * diff
            elif 0.7 < move <= 0.8:
                period += 0.37 * diff
            elif 0.8 < move <= 0.9:
                period += 0.225 * diff
            elif 0.9 < move <= 0.95:
                period += 0.1 * diff
            period = max(0.8,period)
        else:
            move = np.random.rand()
            if move <= 0.045:
                period += 8.5 * diff
            elif 0.045 < move <=0.09:
                period += 7 * diff
            elif 0.09 < move <=0.135:
                period += 5.9 * diff
            elif 0.135 < move <=0.18:
                period += 4.7 * diff
            elif 0.18 < move <=0.225:
                period += 3.5 * diff
            elif 0.225 < move <=0.315:
                period += 2.8 * diff
            elif 0.315 < move <= 0.45:
                period += 1.8 * diff
            elif 0.45 < move <= 0.585:
                period += 0.75 * diff
            elif 0.585 < move <=0.72:
                period += 0.4 * diff
            elif 0.72 < move <= 0.855:
                period += 0.1 * diff
            period = min(575, period)
        if period == 0.8:
            bump = np.random.rand()
            if bump <= 0.25:
                period *= 1 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                period *= 2 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                period *= 3 + np.random.rand()
            else:
                period *= 4 + np.random.rand()
    elif jup_mass >= 4e-2:
        period_epsi = (10/12)*(36/38)
        period = np.random.f(12,36) * (target/period_epsi)
        period *= 0.65
        diff = period - target
        if -target < diff < target:
            if diff < 0:
                period += 0.75*diff
            else:
                period += 10* diff
            period = max(2.5,period)
            period = min(850,period)
            if period == 850:
                bump = np.random.rand()
                if bump <= 0.25:
                    period /= 1 + np.random.rand()
                elif 0.25 < bump <= 0.5:
                    period /= 2 + np.random.rand()
                elif 0.5 < bump <= 0.75:
                    period /= 3 + np.random.rand()
                else:
                    period /= 4 + np.random.rand()
            if period == 2.5:
                bump = np.random.rand()
                if bump <= 0.25:
                    period *= 1 + np.random.rand()
                elif 0.25 < bump <= 0.5:
                    period *= 3 + np.random.rand()
                elif 0.5 < bump <= 0.75:
                    period *= 5 + np.random.rand()
                else:
                    period *= 7 + np.random.rand()
        elif diff < 0:
            move = np.random.rand()
            if move <= 0.2:
                period += 0.3 * diff
            elif 0.2 < move <= 0.4:
                period += 0.15 * diff
            elif 0.4 < move <= 0.5:
                period += 0.1 * diff
            elif 0.5 < move <= 0.6:
                period += 0.075 * diff
            elif 0.6 < move <= 0.8:
                period += 0.05 * diff
            elif 0.8 < move <= 0.9:
                period += 0.025 * diff
            elif 0.9 < move <= 0.95:
                period += 0.01 * diff
            period = max(1.5,period)
            if period == 1.5:
                bump = np.random.rand()
                if bump <= 0.25:
                    period *= 1 + np.random.rand()
                elif 0.25 < bump <= 0.5:
                    period *= 2 + np.random.rand()
                elif 0.5 < bump <= 0.75:
                    period *= 3 + np.random.rand()
                else:
                    period *= 4 + np.random.rand()
        else:
            move = np.random.rand()
            if move <= 0.03125:
                period += 9.5 * diff
            elif 0.03125 < move <= 0.0625:
                period += 9 * diff
            elif 0.0625 < move <= 0.09375:
                period += 8.5 * diff
            elif 0.09375 < move <= 0.125:
                period += 8 * diff
            elif 0.125 < move <= 0.15625:
                period += 7.5 * diff
            elif 0.15625 < move <= 0.1875:
                period += 7 * diff
            elif 0.1875 < move <= 0.21875:
                period += 6.5 * diff
            elif 0.21875 < move <= 0.25:
                period += 6 * diff
            elif 0.25 < move <= 0.3:
                period += 5.5 * diff
            elif 0.3 < move <= 0.35:
                period += 5 * diff
            elif 0.35 < move <= 0.4:
                period += 4.5 * diff
            elif 0.4 < move <= 0.45:
                period += 4 * diff
            elif 0.45 < move <= 0.5:
                period += 3.5 * diff
            elif 0.5 < move <= 0.55:
                period += 3 * diff
            elif 0.55 < move <= 0.6:
                period += 2.5 * diff
            elif 0.6 < move <= 0.65:
                period += 2 * diff
            elif 0.65 < move <= 0.725:
                period += 1.5 * diff
            elif 0.725 < move <= 0.8:
                period += 1.0 * diff
            elif 0.8 < move <= 0.875:
                period += 0.5 * diff
            elif 0.875 < move <= 0.95:
                period += 0.25 * diff
            period = min(850,period)
    mass_epsi = (23/25)*(13/15)
    jup_mass = np.random.f(25,13) * (2/mass_epsi)
    mass_diff = jup_mass - 2
    if mass_diff < 0:
        jup_mass += 0.2 * mass_diff
        jup_mass = max(jup_mass,0.3)
    else:
        jup_mass += 0.2 * mass_diff
        jup_mass = min(jup_mass,20)
    ecc = get_ecc(period)
    deg_inc, rad_inc = get_inclination(period)
    long_asc = np.random.uniform(0,2*np.pi)
    arg_peri = np.random.uniform(0,2*np.pi)
    true_anom = np.random.uniform(0,2*np.pi)

    return (mass, period, ecc, rad_inc, long_asc, arg_peri, true_anom)


#Randomly generate cold jupiter planet
def get_cold_jup():
    mass_epsi = (23/25)*(13/15)
    jup_mass = np.random.f(25,13) * (2/mass_epsi)
    mass_diff = jup_mass - 2
    if mass_diff < 0:
        jup_mass += 0.2 * mass_diff
        jup_mass = max(jup_mass,0.3)
    else:
        jup_mass += 0.2 * mass_diff
        jup_mass = min(jup_mass,20)
    mass = jup_mass / 1047.57
    period_epsi = (5/7) * (64/66)
    period = np.random.f(7,64) * (900/period_epsi)
    period_diff = period - 900
    if period_diff < 0:
        period += 0.15 * period_diff
        period = max(period,50)
        if period == 50:
            bump = np.random.rand()
            if bump <= 0.25:
                mass *= 1 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                mass *= 1.5 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                mass *= 2 + np.random.rand()
            else:
                mass *= 2.5 + np.random.rand()
    else:
        period += 0.2 * period_diff
        period = min(period,6000)
        if period == 6000:
            bump = np.random.rand()
            if bump <= 0.25:
                mass /= 1 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                mass /= 1.5 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                mass /= 2 + np.random.rand()
            else:
                mass /= 2.5 + np.random.rand()

    ecc = get_ecc(period)
    deg_inc, rad_inc = get_inclination(period)

    long_asc = np.random.uniform(0,2*np.pi)
    arg_peri = np.random.uniform(0,2*np.pi)
    true_anom = np.random.uniform(0,2*np.pi)

    return (mass, period, ecc, rad_inc, long_asc, arg_peri, true_anom)


#Randomly generate hot jupiter planet
def get_hot_jup():
    mass_epsi = (86/88) * (11/13)
    jup_mass = np.random.f(88,11) * (1.5/mass_epsi)
    mass_diff = jup_mass - 1.5
    if mass_diff < 0:
        jup_mass += 0.75 * mass_diff
        jup_mass = max(jup_mass,0.3)
    else:
        jup_mass += 1.0 * mass_diff
        jup_mass = min(jup_mass,15)
    mass = jup_mass / 1047.57
    period_epsi = (29/31) * (14/16)
    period = np.random.f(31,14) * (3/period_epsi)
    period_diff = period - 3
    if period_diff < 0:
        period += 0.3 * period_diff
        period = max(period,0.9)
        if period == 0.9:
            bump = np.random.rand()
            if bump <= 0.25:
                mass *= 1 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                mass *= 1.5 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                mass *= 2 + np.random.rand()
            else:
                mass *= 2.5 + np.random.rand()
    else:
        period += 1.0 * period_diff
        period = min(period,40)
        if period == 40:
            bump = np.random.rand()
            if bump <= 0.25:
                mass /= 1 + np.random.rand()
            elif 0.25 < bump <= 0.5:
                mass /= 1.5 + np.random.rand()
            elif 0.5 < bump <= 0.75:
                mass /= 2 + np.random.rand()
            else:
                mass /= 2.5 + np.random.rand()

    ecc = get_ecc(period)

    deg_inc, rad_inc = get_inclination(period)
    long_asc = np.random.uniform(0,2*np.pi)
    arg_peri = np.random.uniform(0,2*np.pi)
    true_anom = np.random.uniform(0,2*np.pi)

    return (mass, period, ecc, rad_inc, long_asc, arg_peri, true_anom)


def generate_system(num_planets, star_mass, only_terr):
    sim = rebound.Simulation()
    sim.units = ("day", "AU", "Msun")
    sim.add(m=star_mass)
    sys_param = np.zeros((num_planets+1,7))
    sys_param[0,0] = star_mass
    if only_terr:
        cold_jup_odds = 0.0
        hot_jup_odds = 0.0
    else:
        if 0.65 <= star_mass <= 1.5:
            cold_jup_odds = 0.8555 / (0.5*num_planets)
        else:
            cold_jup_odds = 0.0
        if 0.31 <= star_mass <= 2.22:
            hot_jup_odds = 0.052961 / (0.5*num_planets)
        else:
            hot_jup_odds = 0.0
    terr_odds = 1.0 - cold_jup_odds - hot_jup_odds
    print(f"terr = {terr_odds}, cold_jup = {cold_jup_odds}, hot_jup={hot_jup_odds}")
    i = 1
    iterations = 0
    while sys_param[num_planets,0] == 0:
        iterations += 1
        if iterations >= 20:
            sorted_sys_param, sim = generate_system(num_planets, star_mass, only_terr)
            return sorted_sys_param, sim
        plan_type = np.random.choice(3,p=[terr_odds,cold_jup_odds,hot_jup_odds])
        if plan_type == 0:
            mass, period, ecc, rad_inc, long_asc, arg_peri, true_anom = get_terrestrial()
        elif plan_type == 1:
            mass, period, ecc, rad_inc, long_asc, arg_peri, true_anom = get_cold_jup()
        elif plan_type == 2:
            mass, period, ecc, rad_inc, long_asc, arg_peri, true_anom = get_hot_jup()

        sim.add(m=mass,P=period,e=ecc,inc=rad_inc,Omega=long_asc,omega=arg_peri,f=true_anom)

        if i == 1:
            sys_param[i,0] = mass
            sys_param[i,1] = period
            sys_param[i,2] = ecc
            sys_param[i,3] = rad_inc
            sys_param[i,4] = long_asc
            sys_param[i,5] = arg_peri
            sys_param[i,6] = true_anom
            i += 1

        else:
            pass_flag = 1
            orbits = sim.calculate_orbits()
            true_anoms = np.linspace(0, 2*np.pi,250)
            x_points = np.empty(len(orbits), dtype="object")
            y_points = np.empty(len(orbits), dtype="object")
            z_points = np.empty(len(orbits), dtype="object")
            for j, o in enumerate(orbits):
                r = o.a * ((1 - o.e**2)/(1 + o.e*np.cos(true_anoms)))
                x_points[j] = r * (np.cos(o.Omega)*np.cos(o.omega+true_anoms) - np.sin(o.Omega)*np.sin(o.omega+true_anoms)*np.cos(o.inc))
                y_points[j] = r * (np.sin(o.Omega)*np.cos(o.omega+true_anoms) + np.cos(o.Omega)*np.sin(o.omega+true_anoms)*np.cos(o.inc))
                z_points[j] = r * (np.sin(o.omega+true_anoms)*np.sin(o.inc))
            for k in range(len(orbits[:-1])):
                x2 = x_points[k]
                y2 = y_points[k]
                z2 = z_points[k]
                x1 = x_points[-1]
                y1 = y_points[-1]
                z1 = z_points[-1]
                d = np.zeros(len(x2)**2)
                n = 0
                for l in range(len(x2)):
                    for m in range(len(x1)):
                        d[n] = np.sqrt((x2[l]-x1[m])**2 + (y2[l]-y1[m])**2 + (z2[l]-z1[m])**2)
                        n += 1
                if d.min() < 3 * max(orbits[1].rhill, orbits[-1].rhill):
                    pass_flag = 0
                    sim.remove(i)
                    break

            if pass_flag == True:
                sys_param[i,0] = mass
                sys_param[i,1] = period
                sys_param[i,2] = ecc
                sys_param[i,3] = rad_inc
                sys_param[i,4] = long_asc
                sys_param[i,5] = arg_peri
                sys_param[i,6] = true_anom
                i += 1

    sorted_sys_param = sys_param[np.concatenate(([0],sys_param[:,1].argsort()[-num_planets:]))]

    sim = rebound.Simulation()
    sim.units = ("day", "AU", "Msun")
    sim.add(m=star_mass)
    for i in range(1,num_planets+1):
        sim.add(m=sorted_sys_param[i,0],P=sorted_sys_param[i,1],e=sorted_sys_param[i,2],inc=sorted_sys_param[i,3],Omega=sorted_sys_param[i,4],omega=sorted_sys_param[i,5],f=sorted_sys_param[i,6])
    sim.move_to_com()
    return sorted_sys_param, sim