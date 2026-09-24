import matplotlib.pyplot as plt
import time

class TimingProfiler:
    def __init__(self, algorithms, inputs, trials):
        self.__algorithms = algorithms
        self.__trials=trials
        self.__inputs=inputs
        self.__results=[]
        self.__string_inputs=[]
        for i in inputs:
            self.__string_inputs.append(str(i))

    @property
    def results(self):
      return self.__results

    def single_experiment(self, algorithm):
        totalTime = 0
        data =[]
        for n in self.__inputs:
            for trial in range(self.__trials):
                if isinstance(n, list) or isinstance(n, tuple):
                    start = time.perf_counter()
                    algorithm(*n)
                else:
                    start = time.perf_counter()
                    algorithm(n)
                stop = time.perf_counter()
                elapsedTime = stop-start
                totalTime += elapsedTime
            data.append(totalTime/self.__trials*1000)
        return data

    def run_experiments(self):
        for algorithm in self.__algorithms:
            result={
                "name": algorithm.__name__,
                "data": self.single_experiment(algorithm)
            }
            self.__results.append(result)

    def graph(self, title="", scale="linear"):
        plt.xscale(scale)
        plt.xlabel('n')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel(f'Time in ms')
        plt.title(title)
        for result in self.__results:
            print()
            plt.plot(self.__string_inputs, result["data"], label = result['name'])
        plt.legend()
        plt.tight_layout()
        plt.show()