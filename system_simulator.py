"""
File: system_simulator.py
Author: Andrew Millar-Wilson

File containing the main modules used in an N body simulation of
planetary movement


"""

#import dependancies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings


#set G
G = 6.6743e-11

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

class System:
    """
    gravitational system class
    instantiates bodies based on user settings (pre-set system or custom)
    """

    
    def __init__(self, system_type = "binary", num_bodies = None, custom_system_info_dict = None): #set as none to allow binary and random systems to be initialised
        if type(num_bodies) == int or num_bodies == None:
            self.num_bodies = num_bodies
        else:
            TypeError("Number of bodies must be an integer")

        valid_system_types = ["random", "binary", "custom"]

        if system_type.lower() in valid_system_types:
            self.system_type = system_type.lower()

            if self.system_type == "random":
                #function to initialise random bodies
                def initialise_random_bodies():
                    """
                    a function which takes in the number of bodies and
                    instantiates a Body
                    """
                    if num_bodies == None:
                        self.num_bodies = np.random.randint(50)
                    else:
                        self.num_bodies = num_bodies

                    self.bodies = []
                    for _ in range(self.num_bodies):
                        #random mass within a reasonable range
                        mass = np.random.uniform(1e9, 1e12)
                        pos = np.random.rand(2) #2D space
                        vel = np.zeros(2) #initial velocity of 0, may be customisable in later updates
                        self.bodies.append(Body(mass, pos, vel))
                
                initialise_random_bodies()

            elif self.system_type == "binary":
                #function to initialise an unstable eliptical binary system
                def initialise_binary_system():
                    self.num_bodies = 2
                    
                    mass_body1 = 2e9  # Mass of the first body
                    mass_body2 = 2e10  # Mass of the second body

                    # Positions and velocities for a stable binary system
                    pos_body1 = np.array([0.2, 0.5])
                    vel_body1 = np.array([0.3, 0.5])

                    pos_body2 = np.array([0.5, 0.5])
                    vel_body2 = np.array([0.0001, 0.0001])

                    body1 = Body(mass_body1, pos_body1, vel_body1)
                    body2 = Body(mass_body2, pos_body2, vel_body2)

                    self.bodies = [body1, body2]
                
                initialise_binary_system()
    
            
            elif self.system_type == "custom":
                def initialise_custom_bodies():
                    #A function to intialise custom systems using the GUI

                    self.custom_system_info_dict = custom_system_info_dict

                    self.num_bodies = len(custom_system_info_dict)

                    self.bodies = []
            
                    for body in custom_system_info_dict:
                        mass = custom_system_info_dict[body]["mass"]
                        pos = np.array(custom_system_info_dict[body]["position"])
                        vel = np.array(custom_system_info_dict[body]["velocity"])
                        self.bodies.append(Body(mass, pos, vel))

                initialise_custom_bodies()
            
            print("System initialised")

        else:
            TypeError(f"System type must be one of {valid_system_types}")

        #system initialised - calculating forces

        #calculate gravitational force between bodies
    def gravitational_force(self, mass1, mass2, pos1, pos2):
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
        
        return(force)

    #update body velocities and positions
    def position_update(self, bodies, dt):
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
                    force = self.gravitational_force(bodies[i].mass, bodies[j].mass, bodies[i].pos, bodies[j].pos)
                    total_force += force
            
            #calculate acceleration (F=ma, rearrange to a=F/m)
            acceleration = total_force / bodies[i].mass

            #implement RK4 method
            k1v = acceleration * dt
            k1x = bodies[i].vel * dt

            k2v = self.gravitational_force(bodies[i].mass, bodies[i].mass, bodies[i].pos + k1x / 2, bodies[i].pos + k1x / 2) / bodies[i].mass * dt
            k2x = (bodies[i].vel + k1v / 2) * dt

            k3v = self.gravitational_force(bodies[i].mass, bodies[i].mass, bodies[i].pos + k2x / 2, bodies[i].pos + k2x / 2) / bodies[i].mass * dt
            k3x = (bodies[i].vel + k2v / 2) * dt

            k4v = self.gravitational_force(bodies[i].mass, bodies[i].mass, bodies[i].pos + k3x, bodies[i].pos + k3x) / bodies[i].mass * dt
            k4x = (bodies[i].vel + k3v) * dt

            #update velocity and position using weghted average
            bodies[i].vel += (k1v + 2 * k2v + 2 * k3v + k4v) /6
            bodies[i].pos += (k1x + 2 * k2x + 2 * k3x + k4x) /6

    def plot_system(self, step=0.01, plot_lims=[[None,None],[None,None]]):
        """
        A function to plot the system caluclated above.
        inputs: 
        N - number of bodies,
        dt - integration step
        plot_lims - plot limits
        """

        #initialise bodies

        #initialise plot
        fig, ax = plt.subplots()
        self.planet_plot = ax.scatter([body.pos[0] for body in self.bodies], [body.pos[1] for body in self.bodies],
                            s=[(body.mass/1e9) for body in self.bodies])
        
        #set X,Y limits - if no limits given, set dynamically by max X and Y position
        if plot_lims==[[None,None],[None,None]]:
            ax.set_xlim(min(body.pos[0] for body in self.bodies) - 0.1, max(body.pos[0] for body in self.bodies) + 0.1)
            ax.set_ylim(min(body.pos[1] for body in self.bodies) - 0.1, max(body.pos[1] for body in self.bodies) + 0.1)

        else:
            ax.set_xlim(plot_lims[0][0], plot_lims[0][1])
            ax.set_xlim(plot_lims[1][0], plot_lims[1][1])


        #set title
        ax.set_title(f'{self.num_bodies} gravitational bodies interacting')

        #add colourbar
        cbar = plt.colorbar(self.planet_plot, ax=ax, label='Velocity Magnitude')
        
        #set integration step
        self.dt = step

        #animate
        animation = FuncAnimation(fig, self.update, frames = 100, interval = 50, blit = True)


        #show animation
        plt.show()

        #clear bodies
        self.bodies = []


    #update plot
    def update(self, frame):
        """
        Function which runs position_update and updates the plot and colour
        """
        self.position_update(self.bodies, self.dt)
        self.planet_plot.set_offsets(np.array([[body.pos[0], body.pos[1]] for body in self.bodies]))
        
        #update colour
        #get absolute vels
        vel_abs = [np.linalg.norm(body.vel) for body in self.bodies]
        
        # Update scatter plot with new colormap based on absolute velocity
        self.planet_plot.set_array(vel_abs)
        self.planet_plot.set_cmap('jet')  # Set the colormap

        #update colourbar limits to ensure distinct colours
        #I have set this up more dynamically previously, but that makes N<3 body simulation colour schemes uninformative 
        self.planet_plot.set_clim(vmin=0, vmax=2)


        return [self.planet_plot]
    

if __name__ == "__main__":
    warnings.warn("This file is not meant to be run - it is called from 'main.py'. Running a binary system as a test of the system simulator")
    system_1 = System("binary")

    system_1.plot_system()


