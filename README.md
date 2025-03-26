<h3 align="center">Gravitational Body Simulator</h3>

  <p align="center">
    Newton first published his laws of gravitation in July 1687, making it possible to predict the movement of gravitaitonal bodies. However, given the complexity of >2 body systems it is still mathematically impossible to predict all future locations of any more than 2 bodies, thus the famous 3 body problem.
    <br />
    <br />
  </p>
  
  <p align="left">
        Though this problem still exists, a model of three or more bodies can be produced by integrating over a series of timesteps, calculating inter-planetary forces at each stage. The equations required for this can be found below.
    <br />
   <br />
   </p>
    
**Newton's Law of Universal Gravitation**

```math
\[ F = \frac{{G \cdot m_1 \cdot m_2}}{{r^2}} \]
```
Where:
- \( F \) is the force of attraction,
- \( G \) is the gravitational constant,
- \( m1 \) and \( m2 \) are the masses of the two objects whose force upon eachother are currently being calculated, and
- \( r \) is the distance between the centers of the two objects.

  <p align="left">
    <br />
      <br />
        The resultant force experienced by each body can then be fed into Newton's second law of motion, Force=mass * acceleration ($F=ma$), reorganised here to $a=F/m$, to calculate the acceleration each body undergoes. This acceleration is then used to calculate the body's updated velocity at each time step, using change in speed = acceleration * time ($\Delta s=a*t$), which is then used to calculate the direction of and distance travelled by the body by, again, multiplying by the integration timestep. These equations are carried out almost simultaneously using the combined function below.
    <br />
    <br />
   </p>
**Change in body velocity**

```math
\[ \Delta v = \frac{{\left(\frac{{G \cdot m_1 \cdot m_2}}{{r^2}}\right)}}{{m_1}}*dt \]
```

**Distance travelled by body**
```math
\[ d = \frac{{\left(\frac{{G \cdot m_1 \cdot m_2}}{{r^2}}\right)}}{{m_1}}*dt^2 \]
```
Implemented as $d = \Delta v * dt$

Where:
- \($\Delta$ v \) is the change in velocity
- \( G \) is the gravitational constant,
- \( m1 \) and \( m2 \) are the masses of the two objects whose force upon eachother are currently being calculated
- \( r \) is the distance between the centers of the two objects.
- \( dt \) is the timestep occuring between each simulation frame, and
- \( d \) is the distance travelled by the body.
</p>
  <p align="left">
    <br />
      <br />
        To maximise accuracy, an RK4 method has been implemented which calculates the changes in velocity 4 times in sequence, passing an adjusted result from the $nth$ layer to the $n+1$ layer, and applies a weighted average, with the first two layers recieving more weight. Though this does increase required compute power, it had no user-discernable impact on performance so was considered a good trade-off.
    <br />
    <br />
   </p>

<h4 align="center">How to run a simulation</h3>
  <p align="left">
    <br />
        For easier user experience, I included a tkinter GUI. To use the GUI-based program, run "main.py". The GUI has two phases, firstly, the desired system configuraiton is picked, from either a rapidly decomposing binary system, a random set of bodies with random positions, masses, and velocities, or a custom system. If the binary or random systems are selected, the simulation will run, however if custom is selected, a new GUI page will appear, prompting the user to input the number of bodies required, then the mass, position, and velocity of each body. After this is completed, the custom simulation will render. See the screen grabs below for a guide.
    <br />
    <b>GUI use</b> 
    <br />
    Step 1: selecting a system
    <br />
  </p>
    <img width="107" alt="screen_1" src="https://github.com/user-attachments/assets/96e43b5a-79c5-4486-ae04-70e65a60236f" />

  <p>
    <br />
    Step 2: (if custom): inputting system details
    <br />
  </p>
  <p>
    <br />
    2a: number of bodies
    <br />
  </p>
    <img width="310" alt="screen_2" src="https://github.com/user-attachments/assets/2398fcd8-d2dc-4933-b16a-6e145c60ee02" />

  <p>
    <br />
    2b: body details
    <br />
  </p>
    <img width="307" alt="screen_3" src="https://github.com/user-attachments/assets/e32a4e7d-9dbd-43f8-9f0b-ab0a0ba9b79a" />

  <p>
    <br />
    Step 3: simulation output (This is a still - the actual output is animated)
    <br />
  </p>
    <img width="479" alt="screen_4" src="https://github.com/user-attachments/assets/ec20b056-5f02-4631-945c-5d09ddbe27ff" />

  <p>
    <br />
    As can be seen in step 3, the output also shows the speed of the body (colour), and the body mass (plotted point size).
    <br />
    <br />
    The custom system can be a little fiddly, so I recommend starting with a two-body system (body 1: mass: 2000000000, position: 0.2, 0.5, velocity: 0.3, 0.5; body 2: mass: 20000000000, position: 0.5, 0.5, velocity: 0.0001, 0.0001). This will output the default binary system, and adjustments can be made as desired.
    <br />
    <br />
    Please contact me if there are any errors or suggestions!
   </p>
</div>


