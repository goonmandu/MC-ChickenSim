import random
from pprint import pformat
import matplotlib.pyplot as plt

def distribute_evenly(num: int, length: int) -> "list[int]":
    '''
    Attempts to divide an integer into parts to indices of a list.
    The list is generated inside this function and is returned.

    :param num: Integer to divide equally.
    :param length: Length of the list to be returned.
    :return: List containing the equally divided argument `num`.
    '''
    # Calculate the base value and the remainder
    base_value = num // length
    remainder = num % length
    
    # Create the list with the base values
    result = [base_value] * length
    
    if remainder > 0:
        # Distribute the remainder across the list
        step = length / remainder
        for i in range(remainder):
            index = round(i * step)
            result[index] += 1
    
    return result

class Coop:
    def __init__(self, adults: int, babies: int, dispenser_rate: float, eqdist: bool = False):
        '''
        Initializes a `Coop` object.
        
        :param adults: Number of adult chickens the coop starts with.
        :param babies: Number of baby chicks the coop starts with.
        :param dispenser_rate: Interval per seconds that the dispenser shoots eggs out.
        :param eqdist: Whether to equally distribute `babies` into the age brackets. (Default `False`: all babies are given age 0.)
        '''
        if adults < 0 or babies < 0 or not isinstance(adults, int) or not isinstance(babies, int):
            raise ValueError("Initial values for adults and babies must be nonnegative integers.")
        if adults + babies < 1:
            raise ValueError("Sum of adults and babies must be positive.")
        if dispenser_rate <= 0:
            raise ValueError("Dispenser rate must be positive.")
        
        self.chickens: dict = {
            "adults": adults,
            "babies": {
                0: babies,
            },
        }
        if not eqdist:
            for age in range(1, 20):
                self.chickens["babies"][age] = 0
        else:
            distribution = distribute_evenly(babies, 20)
            for age in range(20):
                self.chickens["babies"][age] = distribution[age]
        self.time = 0
        self.epm = int(60 / dispenser_rate)
        
    def __str__(self) -> str:
        '''
        String representation of the `Coop` object.
        '''
        a = self.chickens["adults"]
        b = sum(c for c in self.chickens["babies"].values())
        return f"At time {self.time} min,\n" \
               f"Adults: {a}\n" \
               f"Babies: {b}\n" \
               f"Total:  {a + b}\n" \
               f"Baby Chicks Breakdown:\n" \
               f"{pformat(self.chickens['babies'], indent=2)}"
    
    def str_no_breakdown(self) -> str:
        '''
        String representation of the `Coop` object, without baby chicks age bracket breakdown.
        '''
        a = self.chickens["adults"]
        b = sum(c for c in self.chickens["babies"].values())
        return f"At time {self.time} min,\n" \
               f"Adults: {a}\n" \
               f"Babies: {b}\n" \
               f"Total:  {a + b}\n"

    def one_minute(self) -> None:
        '''
        Tick the simulation by 1 minute.
        '''
        # Growing logic
        self.chickens["adults"] += self.chickens["babies"][19]
        for age in range(19, 0, -1):
            self.chickens["babies"][age] = self.chickens["babies"][age-1]
        self.chickens["babies"][0] = 0
        
        # Egg laying and hatching logic
        eggs_laid = int(self.chickens["adults"] / 7.5)  # 5-10 minute egg laying intervals, assuming equal distribution: 1 egg per chicken per 7.5 mins'
        eggs_laid = self.epm if eggs_laid > self.epm else eggs_laid  # Dispenser shoots egg every 0.6 sec
        for _ in range(eggs_laid):
            det = random.randint(1, 256)
            if det == 1:
                self.chickens["babies"][0] += 4  # 1/256 chance to spawn 4 chicks at age 0
            elif 2 <= det <= 32:
                self.chickens["babies"][0] += 1  # 31/256 chance to spawn 1 chick at age 0
            # 192/256 = 3/4 chance to do nothing

        self.time += 1
    
    def less_than_8_adults(self) -> None:
        '''
        Tick the simulation by the minimum number of minutes required for one egg to be dropped by the entire adult chicken population.
        Should not be used when adults >= 8; functionality is and will be untested for this condition.
        '''
        # Fast-forward time so that the sim actually works
        if self.chickens["adults"] > 0:
            minutes_to_ffw = int(7.5 / self.chickens["adults"]) + 1
        else:
            minutes_to_ffw = 20 - max([age for age, count in self.chickens["babies"].items() if count > 0])
        to_become_adults = sum([count for age, count in self.chickens["babies"].items() if age > 19 - minutes_to_ffw])
        self.chickens["adults"] += to_become_adults
        for age in range(19, minutes_to_ffw-1, -1):
            self.chickens["babies"][age] = self.chickens["babies"][age-minutes_to_ffw]
        for age in range(0, minutes_to_ffw):
            self.chickens["babies"][age] = 0

        # Egg laying logic... Let's see how hard this is.
        eggs_laid = int(self.chickens["adults"] * minutes_to_ffw / 7.5)  # 5-10 minute egg laying intervals, assuming equal distribution: 1 egg per chicken per 7.5 mins
        eggs_laid = self.epm * minutes_to_ffw if eggs_laid > self.epm * minutes_to_ffw else eggs_laid  # Dispenser shoots egg every 0.6 sec
        chickens_hatched = 0
        for _ in range(eggs_laid):
            det = random.randint(1, 256)
            if det == 1:
                chickens_hatched += 4  # 1/256 chance to spawn 4 chicks at age 0
            elif 2 <= det <= 32:
                chickens_hatched += 1  # 31/256 chance to spawn 1 chick at age 0
            # 192/256 = 3/4 chance to do nothing
        chicks_to_add_per_age = chickens_hatched // minutes_to_ffw
        leftover_chicks = chickens_hatched % minutes_to_ffw
        for age in range(0, minutes_to_ffw):
            if leftover_chicks > 0:
                self.chickens["babies"][age] += chicks_to_add_per_age + 1
            else:
                self.chickens["babies"][age] += chicks_to_add_per_age
            leftover_chicks =- 1

        self.time += minutes_to_ffw
    
    def sim(self, minutes: int, verbose: bool = False, show_breakdown: bool = True) -> "tuple[list[int], list[int], list[int]]":
        '''
        Simulates the chicken farm and returns statistics per tick of simulation.

        :param minutes: Target minutes to simulate.
        :param verbose: Print per-tick chicken population. (Default `False`: Do not print this information.)
        :param show_breakdown: Print babies' age breakdown alongside verbose logging. Has no effect when `verbose=False`. (Default `True`: Print this information.)
        :return: Tuple containing history of adults and babies population and timestamps recorded in minutes.
        '''
        data = []
        timestamps = []
        data.append(self.get_chickens())
        timestamps.append(self.time)
        while self.chickens["adults"] < 8 and self.time < minutes:
            self.less_than_8_adults()
            data.append(self.get_chickens())
            timestamps.append(self.time)
            if verbose:
                if show_breakdown:
                    print(self)
                else:
                    print(self.str_no_breakdown())
        while self.time < minutes:
            self.one_minute()
            data.append(self.get_chickens())
            timestamps.append(self.time)
            if verbose:
                if show_breakdown:
                    print(self)
                else:
                    print(self.str_no_breakdown())
        adults = [data[i][1] for i in range(len(data))]
        babies = [data[i][2] for i in range(len(data))]
        return adults, babies, timestamps
    
    def get_chickens(self):
        return self.chickens, self.chickens["adults"], sum(c for c in self.chickens["babies"].values())

def plot_population(init_adults: int, init_babies: int, dispenser_rate: float, mins: int) -> None:
    '''
    Show a Matplotlib graph of the chicken population over time.
    
    :param init_adults: Number of adults chickens to start with.
    :param init_babies: Number of baby chicks to start with.
    :param dispenser_rate: Interval per seconds that the dispenser shoots eggs out.
    :param mins: Target minutes to simulate.'''
    coop = Coop(init_adults, init_babies, dispenser_rate=dispenser_rate, eqdist=True)
    adults, babies, x = coop.sim(mins)
    total = [babies[i] + adults[i] for i in range(len(babies))]

    plt.plot(x, babies, label='Babies', color='blue')
    plt.plot(x, total, label='Adults', color='red')
    plt.fill_between(x, 0, babies, color='blue', alpha=0.3)
    plt.fill_between(x, babies, total, color='red', alpha=0.3)
    plt.title(f'Chicken farm population simulation\nStarting with: {init_adults} adults, {init_babies} babies\nEggs/min cap: {coop.epm}')
    plt.xlabel('Time (min)')
    plt.ylabel('Population')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_population(1, 0, 0.6, 360)