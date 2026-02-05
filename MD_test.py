from openmm.app import *
from openmm import *
from openmm.unit import *

# 1. Load your structure
pdb = PDBFile('your_protein.pdb')

# 2. Choose your Force Field
# Amber14 is a standard choice for proteins
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

# 3. System Setup (Add hydrogens and solvent if needed)
modeller = Modeller(pdb.topology, pdb.positions)
modeller.addSolvent(forcefield, padding=1.0*nanometers)

# 4. Create the System
system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME, 
                                 nonbondedCutoff=1.0*nanometer, constraints=HBonds)

# 5. Set up the Integrator and Simulation
integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
simulation = Simulation(modeller.topology, system, integrator)
simulation.context.setPositions(modeller.positions)

# 6. Energy Minimization (Crucial for AI-generated structures!)
print("Minimizing energy...")
simulation.minimizeEnergy()

# 7. Run and Save Results
simulation.reporters.append(PDBReporter('output.pdb', 1000))
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True, 
                            potentialEnergy=True, temperature=True))

print("Running simulation...")
simulation.step(10000)