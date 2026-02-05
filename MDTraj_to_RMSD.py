import mdtraj as md

# Load the trajectory
traj = md.load('output.pdb')

# Calculate RMSD to see if your designed binder stayed stable
rmsd = md.rmsd(traj, traj, 0)
print(rmsd)