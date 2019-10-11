import pytest
from simulation import Simulation

import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
import os

def test_init():
    virus = Virus("Ebola", .25, .70)
    sim = Simulation(100000, .90, virus, initial_infected=10000)
    assert sim.pop_size == 100000
    assert sim.next_person_id == 100
    assert sim.virus == virus
    assert sim.initial_infected == 10000
    assert sim.vacc_percentage == .90
    assert sim.total_dead == 0
    assert sim.newly_dead == []
    assert sim.current_infected == []
    assert sim.newly_infected == []

def test_create_population():
    virus = Virus("Ebola", .25, .70)
    sim = Simulation(100000, .90, virus, initial_infected=10)
    vaccinated = 0
    infected = 0

    for person in sim.population:
        assert person.is_alive == True

        if person.infection is not None:
            infected += 1

        if person.is_vaccinated:
            vaccinated += 1

    assert vaccinated == 90000
    assert infected == 10000
    assert len(sim.population) == 100

def test_simulation_should_continue():
        virus = Virus("Ebola", 0.25, 0.70)
        sim = Simulation(100000, 0.90, virus, 10000)

        for person in sim.population:
            person.is_alive = False
            sim.total_dead += 1
            person.is_vaccinated = False
        assert sim._simulation_should_continue() is True


        for person in sim.population:
            person.is_alive = True
            person.infection = None
            person.is_vaccinated = True
        sim.total_dead = 0
        assert sim._simulation_should_continue() is True

def test_run():
    pass

def test_time_step():
    pass

def test_interaction():
    virus = Virus('Ebola', .25, 0.70)
    sim = Simulation(100000, 0.90, virus, 10000)
    person = Person(1, False)
    sim.population.append(person)
    sim.newly_infected.append(person._id)
    sim._infect_newly_infected()
    assert person.infection == virus

def test_infect_newly_infected():
    pass