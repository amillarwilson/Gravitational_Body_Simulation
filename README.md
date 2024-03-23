<h3 align="center">Gravitational Body Simulator</h3>

  <p align="center">
    Though Newton first published his laws of gravitation in July 1687, given the complexity of >2 body systems it is still mathematically impossible to predict all future locations of any more than 2 bodies, thus the famous 3 body problem, 
    here expanded to an N body problem. 
    <br />
    <br />
  </p>
  
  <p align="left">
        This repo contains code which uses Newton's law of Universal gravitation, and laws of motion, to circumvent this mathematical limit, applying the algorithms below to each body sequentially across time, to instead calculate the movement of each body at each timestep. First, the forces acting on each body from the gravitation of all other bodies is calulcated.
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
        The resultant force experienced by each body can then be fed into Newton's second law of motion, Force=mass * acceleration ($F=ma$), reorganised here to $a=F/m$, to calculate the acceleration each body undergoes. This acceleration is then used to calculate the body's updated velocity at each time step, using change in speed = acceleration * time ($\delta s=a*t$), which is then used to calculate the direction of and distance travelled by the body by, again, multiplying by the integration timestep. These equations are carried out almost simultaneously using the combined function below.
    <br />
    <br />
   </p>
**Change in body velocity**

```math
\[ \delta v = \frac{{\left(\frac{{G \cdot m_1 \cdot m_2}}{{r^2}}\right)}}{{m_1}}*dt \]
```

**Distance travelled by body**
```math
\[ d = \frac{{\left(\frac{{G \cdot m_1 \cdot m_2}}{{r^2}}\right)}}{{m_1}}*dt^2 \]
```
Implemented as $d = \delta v * dt$

Where:
- \(\delta v \) is the change in velocity
- \( G \) is the gravitational constant,
- \( m1 \) and \( m2 \) are the masses of the two objects whose force upon eachother are currently being calculated
- \( r \) is the distance between the centers of the two objects.
- \( dt \) is the timestep occuring between each simulation frame, and
- \( d \) is the distance travelled by the body.

  <p align="left">
    <br />
      <br />
        To maximise accuracy, an RK4 method has been implemented which calculates the changes in velocity 4 times in sequence, passing an adjusted result from the $nth$ layer to the $n+1$ layer, and applies a weighted average, with the first two layers recieving more weight. Though this does increase required compute power, it had no user-discernable impact on performance so was considered a good trade-off.
    <br />
    <br />
   </p>
</div>
