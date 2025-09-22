### Machine 
- Z axis
- XY stage
- Toolhead
	- Pick head
		- 4th axis? probably good idea
	- Camera
	- ?macro camera?
		- Can dieID? 
			- Do we need large camera and real lens? or can we get away with small module and m12 type lens?  
- Up camera for part pick location verification?
- Wafer Frame holder
	- is gravity or similar confinement good enough
		- ? or do we need to have some kind of mechanism to hold/locate
- Overall base/ mount
- 

### Feeders
- 40x feeders total
- Mountable as 20x units
	- individually feedable? 
	- ??or feed with movable feeder thing?
	- 
- Reel take up
	- friction wheels on single bar?
		- I am imagining all reels to fit on a single bar and all reels on like a kebab
			- Similar for tape seal tensioner 
		- These can fit into reel hub and maybe have hex interior
- Tape Sealing
	- Hopefully this can be had by some fancy bent metal
		- Form laser cut steel and anneal
- Feed mechanism
	- Hopefully this can be pin indexed. 
	- If not maybe an indexed pinned wheel if we need more force due to friction from tape sealer
	- last resort individual mechanisms

### Software
- Machine setup/ calibration
	- Find wafer and map dies
		- calibrate machine
	- find feeder locations
- Pick place schema
	- coordinate reticles
	- track pick order and wafer #
	- create pick map
- Die location verification on pick
- Die place verification *in tape*
	- Can we also do dieID verification here too?
- Machine GUI
	- machine state
	- reticle/pick map
	- feeder states and manual control
	- overall completion table/ maybe with visual
- Machine readable data export with reel maps and other useful statistics

### Shipping Crate
- Ideally breaks down to something as small as possible. 

### Stretch Goals
- Automatic wafer frame un/loading
	- simplest version can have 2 slots, one for completed die and one for the next die
	- this can allow the machine to complete and start next die as cycle time is measured in hours
- 
