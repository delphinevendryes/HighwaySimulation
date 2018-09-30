# HighwaySimulation

## Simulation for self-driving

## Classes
- Car, KalmanFilter, ParticleFilter

- Highway

- Message

## Simulation events

At every round (every dt):
- every car sends to every other car noisy information about its position (for now, just exact relative position)
- every car adds information about this round to its information
- every car computes estimate for every other car speed and position

## Complexify model
- later : add multiple lanes (complexify calculations)
- later : every car computes its speed according to the speed of the car in front of it, or changes lane
- later : messages are communicated without car ids -> tracking problem
- later : complexify model for noise variance, maybe it could depend on x_rel

## Test
- Kalman filters
- Particle filters
- Gaussian processes
