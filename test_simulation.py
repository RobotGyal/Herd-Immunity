import pytest
from simulation import Simulation

import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
import os

def test_init():
    pass

def test_create_population():
    virus = Virus("Test", .25, .25)
    sim = Simulation(100, .25, virus, initial_infected=4)
    vaccinated = 0
    infected = 0

    for person in sim.population:
        assert person.is_alive == True

        if person.infection is not None:
            infected += 1

        if person.is_vaccinated:
            vaccinated += 1

    assert vaccinated == 25
    assert infected == 4
    assert len(sim.population) == 100

def test_simulation_should_continue():
    pass

def test_run():
    pass

def test_time_step():
    pass

def test_interaction():
    pass

def test_infect_newly_infected():
    pass