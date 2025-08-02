import time

# Importing these modules will automatically trigger the table generation
# if the files do not already exist. This is part of Herbert Kociemba's
# original design.
print("Starting pattern database and pruning table generation...")
print("This is a one-time process and may take 20-40 minutes.")

start_time = time.time()

# Import the modules that contain the table creation logic
from twophase import pruning
from twophase import symmetries 

end_time = time.time()
duration = end_time - start_time

print("="*50)
print(f"Table generation complete!")
print(f"Process took {duration / 60:.2f} minutes.")
print("The files have been saved to the 'twophase' directory.")
print("You can now copy these files to your submission package.")
