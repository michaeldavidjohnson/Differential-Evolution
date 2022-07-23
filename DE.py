import numpy as np
import copy

def DifferentialEvolution(Function, ParameterBounds, PopulationSize = 10,
                          CrossoverProbability = 0.6, DifferentialWeight = 0.8,
                          Epochs = 100):
  GeneralPopulus = []
  dimensionality = len(ParameterBounds)
  # Initialisation of the populus. (we probably want to vectorise this)
  if not PopulationSize > len(ParameterBounds):
    raise ValueError('Population size mismatch.')
  
  for pop in range(PopulationSize):
    params = []
    for param in ParameterBounds:
      params.append(np.random.uniform(param[0], param[1]))

    GeneralPopulus.append(params)


  for _ in range(Epochs):
    for idx in range(len(GeneralPopulus)):
      potential = copy.copy(GeneralPopulus[idx])
      base = copy.copy(GeneralPopulus[idx])
      a = np.random.choice([idx2 for idx2 in range(len(GeneralPopulus)) if idx2 != idx])

      b = np.random.choice([idx2 for idx2 in range(len(GeneralPopulus)) if idx2 != idx
                            and idx2 != a])

      c = np.random.choice([idx2 for idx2 in range(len(GeneralPopulus)) if idx2 != idx
                            and idx2 != a 
                            and idx2 != b])
      
      a = GeneralPopulus[a]
      b = GeneralPopulus[b]
      c = GeneralPopulus[c]
      ForcedSwitch = np.random.choice(range(dimensionality))
      

      for _ in range(dimensionality):  
        if _ == ForcedSwitch or np.random.uniform() < CrossoverProbability:
          potential[_] = (a[_] + DifferentialWeight * (b[_] - c[_]))
          
          if potential[_] > ParameterBounds[_][1]:
            potential[_] = ParameterBounds[_][1]
          
          if potential[_] < ParameterBounds[_][0]:
            potential[_] = ParameterBounds[_][0]
        
      potential_value = Function(potential)
      
      if potential_value < Function(GeneralPopulus[idx]):
        GeneralPopulus[idx] = potential
      
      else:
        GeneralPopulus[idx] = GeneralPopulus[idx]

      

  best_fun = Function(GeneralPopulus[0])
  best_pos = GeneralPopulus[0]
  for gen in GeneralPopulus:
    if Function(gen) <= best_fun:
      best_fun = Function(gen)
      best_pos = gen
  return best_pos, best_fun
