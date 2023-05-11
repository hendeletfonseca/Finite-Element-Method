import numpy as np
import json

def readMesh():
  with open("input.json") as f:
    data = json.load(f)
  for key in data:
    data[key] = np.array(data[key])
  return data["nodes"], data["elems"], data["forces"], data["props"], data["restrs"]

def main():
  nodes, elems, forces, props, restrs = readMesh()
  NNodes = len(nodes)
  NElems = len(elems)
  K = np.zeros((NNodes, NNodes))
  
  for e in range(NElems):
    coordsE = np.array([elems[e, 0] - 1, elems[e, 1] - 1])
    ke = stiffness(props[e], coordsE)
    for i in range(2):
      for j in range(2):
        K[elems[e,i] - 1, elems[e,j] - 1] += ke[i,j]
  
  for i in range(len(restrs)):
    if restrs[i] == 1:
      K[i, ] = 0
      K[i,i] = 1
      forces[i] = 0

  D = np.linalg.solve(K,forces)
  print(K)
  print(D)

def stiffness(props, coords):
  E = props[0]
  A = props[1]
  L = abs(coords[0] - coords[1])
  return np.array([[(E*A/L), -(E*A/L)],[-(E*A/L), (E*A/L)]])

if __name__ == "__main__":
  main()