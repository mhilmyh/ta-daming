TOTAL_POPULATION = 60_360_000           # 60.36 juta

ALPHA = 0.3
BETA = 0.6
GAMMA = 0.1
DELTA = 0.1
RHO = 0.1
RO = 3.0

D0 = 7
R0 = 1
I0 = 127
E0 = 94
S0 = TOTAL_POPULATION - E0 - I0 - R0 - D0

INFECTION_TIME = 14                     # 2 minggu
INCUBATION_TIME = 7
START_LOCKDOWN = 1
TIME_BEFORE_DEATH = 21                  # 3 minggu

TIME = 30 * 12                          # 1 tahun
TIMESTEP = TIME
