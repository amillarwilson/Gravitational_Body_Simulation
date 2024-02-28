"""
File containing the main modules used in an N body simulation of
planetary movement


"""

#import dependancies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#set G
G = 6.6743e-11

#calculate gravitational force between bodies
def gravitational_force(mass1, mass2, pos1, pos2):
    """
    This function takes in the mass and position of bodies and uses F=Gmm/r^2
    to calculate gravitational force between bodies
    """
    #distance between bodies
    r = np.linalg.norm(pos2-pos1)

    # Adding a check to avoid division by zero
    if r < 1e-6:
        return np.zeros_like(pos1)

    #force
    f_magnitude = G * (mass1 * mass2) / (r**2)
    f_direction = (pos2-pos1) / r
    force = f_magnitude * f_direction
    return force

#update body velocities and positions

def position_update(bodies, dt):
    """
    This function takes in a list of bodies and dt, the integral timestep
    using the RK4 method for integration here as it affords higheraccuracy than the Eular method
    """
    num_bodies = len(bodies)

    for i in range(num_bodies):
        #initialise force - 2d simulation
        total_force = np.zeros(2)

        #force calculation
        for j in range(num_bodies):
            #handle case where forces are calculated on the same object
            if i !=j:
                force = gravitational_force(bodies[i].mass, bodies[j].mass, bodies[i].pos, bodies[j].pos)
                total_force += force
        
        #calculate acceleration (F=ma, rearrange to a=F/m)
        acceleration = total_force / bodies[i].mass

        #implement RK4 method
        k1v = acceleration * dt
        k1x = bodies[i].vel * dt

        k2v = gravitational_force(bodies[i].mass, bodies[i].mass, bodies[i].pos + k1x / 2, bodies[i].pos + k1x / 2) / bodies[i].mass * dt
        k2x = (bodies[i].vel + k1v / 2) * dt

        k3v = gravitational_force(bodies[i].mass, bodies[i].mass, bodies[i].pos + k2x / 2, bodies[i].pos + k2x / 2) / bodies[i].mass * dt
        k3x = (bodies[i].vel + k2v / 2) * dt

        k4v = gravitational_force(bodies[i].mass, bodies[i].mass, bodies[i].pos + k3x, bodies[i].pos + k3x) / bodies[i].mass * dt
        k4x = (bodies[i].vel + k3v) * dt

        #update velocity and position using weghted average
        bodies[i].vel += (k1v + 2 * k2v + 2 * k3v + k4v) /6
        bodies[i].pos += (k1x + 2 * k2x + 2 * k3x + k4x) /6


#create class which represents a planetary body
class Body:
    """
    Planetary body class
    instantiates with mass, position, velicty

    """
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.pos = pos
        self.vel = vel
    
#function to initialise random bodies
def initialise_random_bodies(num_bodies):
    """
    a function which takes in the number of bodies and
    instantiates a Body
    """
    bodies = []
    for _ in range(num_bodies):
        #random mass within a reasonable range
        mass = np.random.uniform(1e9, 1e12)
        pos = np.random.rand(2) #2D space
        vel = np.zeros(2) #initial velocity of 0, may be customisable in later updates
        bodies.append(Body(mass, pos, vel))
    return bodies

#function to initialise an unstable eliptical binary system
def initialise_binary_system():
    mass_body1 = 2e9  # Mass of the first body
    mass_body2 = 2e10  # Mass of the second body

    # Positions and velocities for a stable binary system
    pos_body1 = np.array([0.2, 0.5])
    vel_body1 = np.array([0.3, 0.5])

    pos_body2 = np.array([0.5, 0.5])
    vel_body2 = np.array([0.0001, 0.0001])

    body1 = Body(mass_body1, pos_body1, vel_body1)
    body2 = Body(mass_body2, pos_body2, vel_body2)

    return [body1, body2]

#update plot
def update(frame):
    """
    Function which runs position_update and updates the plot
    """
    position_update(bodies, dt)
    scatter.set_offsets(np.array([[body.pos[0], body.pos[1]] for body in bodies]))

    return [scatter]
    



#sections to move to main running file and possibly refactor or add to TKINTER to make it more accessible
#so far there are two sims: 4 random bodies and an eliptical, unstable orbit like a black hole
#I need to refactor the simulation calls later to easily call the function, will also make
#GUi-ing the thing easier

#random bodies

#set "N"
n_bodies = 4

#initialise bodies
bodies = initialise_random_bodies(n_bodies)


#initialise plot
fig, ax = plt.subplots()
scatter = ax.scatter([body.pos[0] for body in bodies], [body.pos[1] for body in bodies])
ax.set_title('4 Randomly positioned bodies')
#dynamically set axis limits so the plot focuses in on the action
ax.set_xlim(min(body.pos[0] for body in bodies) - 0.1, max(body.pos[0] for body in bodies) + 0.1)
ax.set_ylim(min(body.pos[1] for body in bodies) - 0.1, max(body.pos[1] for body in bodies) + 0.1)

#set integration step
dt = 0.001

#animate
animation = FuncAnimation(fig, update, frames = 100, interval = 50, blit = True)


#show animation
plt.show()

#clear bodies
bodies = []

#binary system

n_bodies = 2

#initialise bodies
bodies = initialise_binary_system()


#initialise plot
fig, ax = plt.subplots()
scatter = ax.scatter([body.pos[0] for body in bodies], [body.pos[1] for body in bodies])
ax.set_title('An unstable binary system')
#static axis limits, the smulation will behave the same way each time and the best action occurs between 0,0 and 1,1
ax.set_xlim(0,1)
ax.set_ylim(0,1)

#set integration step
dt = 0.01

#animate
animation = FuncAnimation(fig, update, frames = 100, interval = 50, blit = False)


#show animation
plt.show()

#clear bodies
bodies = []

#to do: 
#2) move all code after line 109 to dedicated running script