import numpy as np

# modes: forward, turn, collect, stop,
# start driving if in decision step
def set_start_position(Rover):
    if Rover.count == 1:
        Rover.starting_position = Rover.pos

def manage_previous_positions(Rover):
    # Store previous position
    if len(Rover.previous_positions) < 10:
        Rover.previous_positions.append(Rover.pos)
    else:
        # overwrite the last position
        Rover.previous_positions[9] == Rover.pos
        for x in range(0,8):
            Rover.previous_positions[x-1] = Rover.previous_positions[x]

# put all code in functions
def decision_step(Rover):
    # increment the counter Rover.count
    # set the starting position
    set_start_position(Rover)
    Rover.count += 1
    manage_previous_positions(Rover)
    # incoming visual data so Rover can decide.
    if Rover.nav_angles is not None:
        # Rover is in forward mode.
        # check if Rover is stuck
        check_stuck(Rover)
        if Rover.mode == 'stuck':
            # must back up and turn
            backup_and_turn(Rover)
        if Rover.mode == 'forward':
            #  enough navigable pixels ahead so drive.
            if can_move_forward(Rover):
                drive(Rover)
        #  not enough navigable pixels ahead so enter stop mode.
        elif cannot_move_forward(Rover):
            stop(Rover)
        # Rover is in stop mode.
        if Rover.mode == 'stop':
            # Has the Rover stopped already?
            if not stopped(Rover):
                # if not then keep stopping.
                stop(Rover)
            # if stopped.
            elif stopped(Rover):
                # can Rover move forward?
                if cannot_move_forward(Rover):
                    # cannot move forward so turn.
                    turn(Rover)
                # can move forward then drive.
                if can_move_forward(Rover):
                    drive(Rover)
    # other situation.
    else:
        # at all times back up when you see no navigable pixels
        if len(Rover.nav_angles) <= 20:
            mode = 'stuck'
        if Rover.mode == 'stuck':
            backup_and_turn(Rover)
        else:
            Rover.throttle = Rover.throttle_set
            Rover.steer = 0
            Rover.brake = 0

    return Rover



####
# Rover functions, the actions the Rover can take.
####    
def drive_to_goal(Rover, goal):
    # the goal are the coordinates (x,y), to navigate to.
    # move in the direction of the goal

    if Rover.vel < Rover.max_vel:
        # Set throttle value to throttle setting
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    Rover.brake = 0
    # Set steering to average angle clipped to the range +/- 15
    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
    Rover.mode = 'forward'


def backup_and_turn(Rover):

    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
    if Rover.vel > 0.2:
        Rover.brake = Rover.brake_set
    if Rover.vel < 0.2:
        Rover.brake = 0
        Rover.throttle = -(Rover.throttle_set)
        Rover.mode = 'stop'
    # turn until you see navigable terrain then stop turning
    if len(Rover.nav_angles) > 20:
        Rover.mode = 'forward'
        drive(Rover)

def check_stuck(Rover):
    if len(Rover.nav_angles) <= 20:
        Rover.mode = 'stuck'
    if (Rover.vel >= 0.1 or Rover.vel <= -0.1):
        count = 0
        for position in Rover.previous_positions:
            if int(position[0]) == int(Rover.pos[0]) and int(position[1]) == int(Rover.pos[1]):
                count += 1
                print("count is now %d" %count)
            if count > 2:
                Rover.mode = 'stuck'

# make a more sophisticated turn function, but how?
# what is the best way to turn?
def turn(Rover):
    Rover.throttle = 0
    # Release the brake to allow turning
    Rover.brake = 0
    # Turn range is +/- 15 degrees,
    # when stopped the next line will induce 4-wheel turning
    Rover.steer = -15 # Could be more clever here about which way to turn

def stopped(Rover):
    if Rover.vel <= 0.2:
        return True
    return False

def cannot_move_forward(Rover):
    return len(Rover.nav_angles) < Rover.stop_forward


def can_move_forward(Rover):
    # Check the extent of navigable terrain
    return len(Rover.nav_angles) >= Rover.stop_forward


# rock grabbing when do you set it in action
def collect_rock(Rover):
    # locate the sample

    # drive to the sample slowly

    # stop at sample

    # collect sample

    # switch to driving mode
    pass


def stop(Rover):
    # Set mode to "stop" and hit the brakes!
    Rover.throttle = 0
    # Set brake to stored brake value
    Rover.brake = Rover.brake_set
    Rover.steer = 0
    Rover.mode = 'stop'

# just cruising
def drive(Rover):

    if Rover.vel < Rover.max_vel:
        # Set throttle value to throttle setting
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    Rover.brake = 0
    # Set steering to average angle clipped to the range +/- 15
    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
    Rover.mode = 'forward'
