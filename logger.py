from person import Person
from virus import Virus
import os.path

class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''

    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        with open(self.file_name, 'w') as log_file:
            log_file.write(f"{pop_size}\t{vacc_percentage}\t{virus_name}\t{mortality_rate}\t{basic_repro_num}\n")

    def log_interaction(self, person, random_person, random_person_sick=None, random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        with open(self.file_name, 'a') as log_file:
            if did_infect:
                log = f"{person._id} infects {random_person._id}.\n"
            else:
                log = f"{person._id} did not infect {random_person._id}.\n"

                if random_person_sick:
                    log += '- already sick.\n'
                elif random_person_vacc:
                    log += '— already vaccinated.\n'

            log_file.write(log)

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        if person.is_alive:
            did_die_from_infection = False
            log = f"{person._id} survived infection.\n"
        else:
            did_die_from_infection = True
            log = f"{person._id} died from infection.\n"

        with open(self.file_name, 'a') as log_file:
            log_file.write(log)

    def log_time_step(self, time_step_number, new_inf, new_dead, t_inf, t_dead):
        ''' STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        with open(self.file_name, 'a') as log_file:
            log_file.write(f"\nTime step {time_step_number} ended..\n{new_inf} people were infected\n{new_dead} people died\n{t_inf} total infected\n{t_dead} total dead\n{time_step_number+1} beginning..")


## TEST SUITE ##
def test_logger_instantiation():
    data = Logger('logger.txt')

    assert os.path.isfile('logger.txt') is True
    assert data.file_name == 'logger.txt'

def test_write_metadata():
    data = Logger('logger.txt')

    data.write_metadata(100000, 0.90, 'Ebola', 0.70, 0.25)

    with open(data.file_name, 'r+') as file:
        in_file = file.read()
        file.seek(0)
        file.truncate()

    expected = '100000\t0.9\tEbola\t0.7\t0.25\n'

    assert in_file == expected

def test_log_interaction():
    data = Logger('logger.txt')
    virus = Virus('HIV', 0.8, 0.3)
    person1 = Person(1, False, virus)
    random_person = Person(2, False)

    data.log_interaction(person1, random_person, False, random_person.is_vaccinated, True)

    with open(data.file_name, 'r+') as file:
        in_file = file.read()
        file.seek(0)
        file.truncate()

    expected = '1 infects 2.\n'

    assert in_file == expected

def test_log_infection_survival():
    data = Logger('logger.txt')
    virus = Virus('HIV', 0.8, 0.3)
    person = Person(1, False, virus)

    survived = person.did_survive_infection()
    data.log_infection_survival(person, survived)

    with open(data.file_name, 'r+') as file:
        in_file = file.read()
        file.seek(0)
        file.truncate()

    expected = '1 survived infection.\n'
    assert in_file == expected

def test_log_time_step():
    data = Logger('logger.txt')

    data.log_time_step(5, 85, 25, 1223, 656)

    with open(data.file_name, 'r+') as file:
        in_file = file.read()
        file.seek(0)
        file.truncate()

        expected = '\nTime step 5 ended..\n85 people were infected\n25 people died\n1223 total infected\n656 total dead\n6 beginning..'

        assert in_file == expected


if __name__ == '__main__':
    test_logger_instantiation()
    test_write_metadata()
    test_log_interaction()
    test_log_infection_survival()
    test_log_time_step()

