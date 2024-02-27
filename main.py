import math 
# from random import random
import numpy as np
from typing import Callable

RandVarFunct = Callable[[], float]

# def uniform(a: float, b: float) -> float:
#     return a + (b - a) * random()

# def exponential(alpha: float) -> float:
#     return - math.log(uniform(0, 1)) / alpha

class Simulation:
    def __init__(
        self, total_time: float, number_servers: int, 
        sim_arrive: RandVarFunct, sim_services: list[RandVarFunct]
    ) -> None:
        self._total_time = total_time
        self._number_servers = number_servers
        self._sim_arrive = sim_arrive
        self._sim_services = sim_services

    def simulate(self):
        time_arrival = 0 # Arrivals Times
        t_events = np.full(self._number_servers, math.inf) # Events times by each server
        number_arrivals = number_departures = 0
        times_in_servers  = [[] for _ in range(self._number_servers)] # Historical of times in each server
        clients_in_service = np.zeros(self._number_servers, dtype=int) # Number of clients in service by each server 
        
        next_arrival = time_arrival = self._sim_arrive()
        time = 0 # global time
        
        while time_arrival <= self._total_time:
            curr_server = np.argmin(t_events) # server with the next event

            # if the next arrival comes before the others events 
            if time_arrival <= t_events[curr_server]:
                # execute the arrival event
                time += time_arrival
                number_arrivals += 1
                clients_in_service[0] += 1
                times_in_servers[0].append(time)
                
                # generate the next arrival
                next_arrival = self._sim_arrive()
                time_arrival = time + next_arrival
                
                # if the server just has a client, generate the next arrival 
                if clients_in_service[0] == 1:
                    t_events[0] = time + self._sim_services[0]()
            
            # execute an change of server
            else:
                time += t_events[curr_server]
                clients_in_service[curr_server] -= 1
                
                if clients_in_service[curr_server] > 0:
                    t_events[curr_server] = time + self._sim_services[curr_server]()
                else:
                    t_events[curr_server] = math.inf
                    
                if curr_server >= self._number_servers - 1:
                    number_departures += 1
                else:
                    clients_in_service[curr_server + 1] += 1
                    times_in_servers[curr_server + 1].append(time)

                    if clients_in_service[curr_server + 1] == 1:
                        t_events[curr_server + 1] = time + self._sim_services[curr_server + 1]()


        # Process the rest of clients
        while number_arrivals < number_departures:
            curr_server = np.argmin(t_events)
            time += t_events[curr_server]
            clients_in_service[curr_server] -= 1
            
            if clients_in_service > 0:
                t_events[curr_server] = time + self._sim_services[curr_server]()
            else:
                t_events[curr_server] = math.inf
                
            if curr_server >= self._number_servers - 1:
                number_departures += 1
            else:
                clients_in_service[curr_server + 1] += 1
                times_in_servers[curr_server + 1].append(time)
                
                if clients_in_service[curr_server + 1] == 1:
                    t_events[curr_server + 1] = time + self._sim_services[curr_server + 1]()

        return times_in_servers 



servers = [
    lambda: np.random.uniform(),
    lambda: np.random.exponential(0.2),
    lambda: np.random.chisquare(0.1),
    lambda: np.random.uniform(0.4),
    lambda: np.random.exponential(0.5),
]
sim = Simulation(1440, 5, lambda: np.random.exponential(0.5), servers)
times = sim.simulate()

print('===========================')
print(times)
print('===========================')

print(times[-1][-1])
print(times[0][-1])

    
    
    