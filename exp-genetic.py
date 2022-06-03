# Experimental implementation of simple genetic scheduling algorithm.

# Based on: https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/

################################################################
# Simple scheduler using a genetic algorithm.
# Assigns courses to timeslots.
# Assigns professors to courses.
# Courses in the same year may not occupy overlapping timeslots.
# Professors may only teach courses for which they are qualified.


from cmath import inf
from numpy.random import randint
from numpy.random import rand
import random
import copy


class Course:
    def __init__(self, name = None, year = None, timeslot = None, instructor = None):
        self.name_ = name
        self.year_ = year
        self.timeslot_ = timeslot
        self.instructor_ = instructor

class TimeSlot:
    def __init__(self, start = None):
        self.start_ = start 

class Instructor:
    def __init__(self, name = None, qualifications = None):
        self.name_ = name
        self.qualifications_ = qualifications

class Timetable:
    def __init__(self, courses_in = None, fitness_in = None):
        self.listing_ = courses_in
        self.fitness_ = fitness_in


# Define algorithm data elements.
courses = [Course("CSC111", 1), Course("MATH100", 1), Course("PHYS110", 1),
            Course("CSC230", 2), Course("SENG265", 2), Course("STAT260", 2),
            Course("CSC361", 3), Course("ECE360", 3), Course("SENG321", 3),
            Course("SENG480A", 4), Course("SENG480B", 4), Course("SENG480C", 4)]

instructors = [Instructor("instructor_1", ["CSC111", "MATH100", "PHYS110"]),
                Instructor("instructor_2", ["CSC230", "SENG265", "STAT260"]),
                Instructor("instructor_3", ["CSC361", "ECE360", "SENG321"]),
                Instructor("instructor_4", ["SENG480A", "SENG480B", "SENG480C"])]

timeslots = [TimeSlot(830), TimeSlot(930), TimeSlot(1030)]


# Objective function. Evaluates the fitness of a schedule.
# This is where constraints are implemented.
def evaluate(schedule):
    fitness = 0

    # Instructors may only teach courses for which they are qualified.
    for course in schedule.listing_:
        if course.name_ not in course.instructor_.qualifications_:
            fitness = fitness - 1
        else:
           pass 

    # Courses within the same academic year cannot overlap
    # ie 1st year courses can't overlap with other 1st year courses, etc.
    first_year_courses_times = [x.timeslot_.start_ for x in schedule.listing_ if x.year_ == 1]
    if (len(set(first_year_courses_times)) != len(first_year_courses_times)):
        fitness = fitness - 1
    
    second_year_courses_times = [x.timeslot_.start_ for x in schedule.listing_ if x.year_ == 2]
    if (len(set(second_year_courses_times)) != len(second_year_courses_times)):
        fitness = fitness - 1
    
    third_year_courses_times = [x.timeslot_.start_ for x in schedule.listing_ if x.year_ == 3]
    if (len(set(third_year_courses_times)) != len(third_year_courses_times)):
        fitness = fitness - 1
    
    fourth_year_courses_times = [x.timeslot_.start_ for x in schedule.listing_ if x.year_ == 4]
    if (len(set(fourth_year_courses_times)) != len(fourth_year_courses_times)):
        fitness = fitness - 1

    schedule.fitness_ = fitness
    return fitness
 

# Tournament selection. Selects a schedule for use in crossover. Schedules with higher fitness have higher probability of being selected.
# def selection(pop, k=10):
# 	# First random selection
# 	selection_ix = randint(len(pop))
# 	for ix in randint(0, len(pop), k-1):
# 		# Check if better (e.g. perform a tournament)
# 		if pop[ix].fitness_ < pop[selection_ix].fitness_:
# 			selection_ix = ix
# 	return pop[selection_ix]
 

# Crossover two parents to create two children.
def crossover(p1, p2, r_cross):
    c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
    
    if rand() < r_cross:
        # Select crossover point that is not on the end of the string
        pt = randint(1, len(p1.listing_) - 2)
        # Perform crossover
        if rand() < 0.5:
            c1.listing_ = copy.deepcopy(p1.listing_[:pt]) + copy.deepcopy(p2.listing_[pt:])
            c2.listing_ = copy.deepcopy(p2.listing_[:pt]) + copy.deepcopy(p1.listing_[pt:])
        else:
            c1.listing_ = copy.deepcopy(p2.listing_[:pt]) + copy.deepcopy(p1.listing_[pt:])
            c2.listing_ = copy.deepcopy(p1.listing_[:pt]) + copy.deepcopy(p2.listing_[pt:])   

    return [c1, c2]
 
# Mutation operator. Randomly reassigns the instructor and timeslot of a schedule.
def mutation(schedule, r_mut):
    for i in range(len(schedule.listing_)):
        # Check for a mutation
        if rand() < r_mut:
            schedule.listing_[i].timeslot_ = random.choice(timeslots)
            schedule.listing_[i].instructor_ = random.choice(instructors)

# Genetic algorithm.
def genetic_algorithm(objective, n_iter, n_pop, n_cross, r_cross, r_mut):

    # Create initial population of schedules having random assignments of timeslot and instructor to courses.
    pop = []
    for i in range(n_pop):
        schedule = Timetable()
        schedule.listing_ = copy.deepcopy(courses)
        for course in schedule.listing_:
            course.instructor_ = random.choice(instructors)
            course.timeslot_ = random.choice(timeslots)
        pop.append(schedule)

    # Keep track of best solution.
    best, best_eval = [], objective(pop[0])

    # Iteratively produce child schedules.
    # n_cross children are produced each iteration.
    # These children replace the schedules in the current generation having the lowest fitness.
    for gen in range(n_iter):
        # Evaulate all schedules in current population.
        for schedule in pop:
            objective(schedule) 

        # Sort the populations in descending order of fitness.
        def getFitness(schedule):
            return schedule.fitness_
        pop.sort(reverse=True, key=getFitness)

        # Check for new best solution
        if (pop[0].fitness_ > best_eval):
            best, best_eval = pop[0], pop[0].fitness_
            print("new best: " + str(best_eval))
            if best_eval == 0:
                break

        # Select parents for reproduction. The first n_cross populations are the fittest, since pop[] is sorted by fitness.
        selected = pop[:n_cross]

        # Create the next generation
        children = []
        for i in range(0, n_cross, 2):
            # Get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # Crossover and mutation
            for schedule in crossover(p1, p2, r_cross):
                # Mutation
                mutation(schedule, r_mut)
                # Store for next generation
                children.append(schedule)

        # Replace the least fit individuals in the population.
        for i in range(n_cross):
            pop.pop()
        pop = pop + children

    return [best, best_eval]
 
# Define the total iterations
n_iter = 500
# Bits
n_courses = len(courses)
# Define the population size
n_pop = 100
# Number of new candidates produced in each generation.
n_cross = 10
# Crossover rate
r_cross = 0.9
# Mutation rate
r_mut = 0.1
# Perform the genetic algorithm search
# genetic_algorithm(evaluate, n_iter, n_pop, r_cross, r_mut)
best, score = genetic_algorithm(evaluate, n_iter, n_pop, n_cross, r_cross, r_mut)

# Print results
print('Done!')
print()
print('Timetable:')
for course in best.listing_:
    print(course.name_ + ": " + course.instructor_.name_ + ": " + str(course.timeslot_.start_))
print("Fitness: " + str(score))
print()


################################################################
# Basic genetic algorithm example. Solves the traveling salesman problem.


# # objective function
# def onemax(x):
# 	return -sum(x)

# # Tournament selection
# def selection(pop, scores, k=3):
# 	# first random selection
# 	selection_ix = randint(len(pop))
# 	for ix in randint(0, len(pop), k-1):
# 		# check if better (e.g. perform a tournament)
# 		if scores[ix] < scores[selection_ix]:
# 			selection_ix = ix
# 	return pop[selection_ix]
 
# # crossover two parents to create two children
# def crossover(p1, p2, r_cross):
# 	# children are copies of parents by default
# 	c1, c2 = p1.copy(), p2.copy()
# 	# check for recombination
# 	if rand() < r_cross:
# 		# select crossover point that is not on the end of the string
# 		pt = randint(1, len(p1)-2)
# 		# perform crossover
# 		c1 = p1[:pt] + p2[pt:]
# 		c2 = p2[:pt] + p1[pt:]
# 	return [c1, c2]
 
# # mutation operator
# def mutation(bitstring, r_mut):
# 	for i in range(len(bitstring)):
# 		# check for a mutation
# 		if rand() < r_mut:
# 			# flip the bit
# 			bitstring[i] = 1 - bitstring[i]
 
# # genetic algorithm
# def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut):
	
#     # initial population of random bitstring
# 	pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]

# 	# keep track of best solution
# 	best, best_eval = 0, objective(pop[0])

# 	# enumerate generations
# 	for gen in range(n_iter):

# 		# evaluate all candidates in the population
# 		scores = [objective(c) for c in pop]

# 		# check for new best solution
# 		for i in range(n_pop):
# 			if scores[i] < best_eval:
# 				best, best_eval = pop[i], scores[i]
# 				print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))

# 		# select parents
# 		selected = [selection(pop, scores) for _ in range(n_pop)]

# 		# create the next generation
# 		children = list()
# 		for i in range(0, n_pop, 2):

# 			# get selected parents in pairs
# 			p1, p2 = selected[i], selected[i+1]

# 			# crossover and mutation
# 			for c in crossover(p1, p2, r_cross):
# 				# mutation
# 				mutation(c, r_mut)
# 				# store for next generation
# 				children.append(c)

# 		# replace population
# 		pop = children
# 	return [best, best_eval]
 
# # define the total iterations
# n_iter = 100
# # bits
# n_bits = 20
# # define the population size
# n_pop = 100
# # crossover rate
# r_cross = 0.9
# # mutation rate
# r_mut = 1.0 / float(n_bits)
# # perform the genetic algorithm search
# best, score = genetic_algorithm(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)
# print('Done!')
# print('f(%s) = %f' % (best, score))






