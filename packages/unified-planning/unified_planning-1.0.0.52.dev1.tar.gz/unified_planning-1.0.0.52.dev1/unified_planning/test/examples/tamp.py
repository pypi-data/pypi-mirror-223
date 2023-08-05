# Copyright 2021-2023 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import math
from unified_planning.shortcuts import *
from collections import namedtuple

Example = namedtuple("Example", ["problem", "plan"])

FILE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_example_problems():
    problems = {}

    # assumptions:
    # 1. the world is deterministic
    # 2. the world is completely known
    # 3. the moveable object (e.g., the robot) moves in a map composed of fixed obstacles
    # 4. there is one common reference system (e.g., /world (0.0, 0.0, 0.0)) - that is the reference system of the map

    Robot = MovableType("robot")

    # representation of the free and occupied working space, fixed obstacles are located on the occupied areas (e.g., Octomap)
    map = OccupancyMap(os.path.join(FILE_PATH, "..", "tamp", "test-map.yaml"), (0, 0))

    # representation of the state of a movable object
    # the input is equals to the number of variables useful to define this state
    # (e.g., 3 = [x, y, yaw] - N = [N-DOFs of a robot])
    RobotConfig = ConfigurationType("robot_config", map, 3)

    robot_at = Fluent("robot_at", BoolType(), robot=Robot, configuration=RobotConfig)

    # configurations in the map
    # map and RobotConfig added for consistency check
    # e.g., `c1` is a configuration expressed via 5 variables and is a collision free configuration in `map`
    c1 = ConfigurationObject("c1", RobotConfig, (4.0, 26.0, 3 * math.pi / 2.0))
    c2 = ConfigurationObject("c2", RobotConfig, (26.0, 26.0, math.pi / 2.0))

    r1 = MovableObject(
        "r1",
        Robot,
        footprint=[(-1.0, 0.5), (1.0, 0.5), (1.0, -0.5), (-1.0, -0.5)],
        motion_model=MotionModels.REEDSSHEPP,
        parameters={"turning_radius": 4.0},
    )

    move = InstantaneousMotionAction(
        "move", robot=Robot, c_from=RobotConfig, c_to=RobotConfig
    )
    robot = move.parameter("robot")
    c_from = move.parameter("c_from")
    c_to = move.parameter("c_to")
    move.add_precondition(robot_at(robot, c_from))
    move.add_effect(robot_at(robot, c_from), False)
    move.add_effect(robot_at(robot, c_to), True)

    # there exists a motion control in your motion model that lets the moveable object moves from c_from to [c_to],
    # where [c_to] is a set of waypoints in your map
    move.add_motion_constraint(Waypoints(robot, c_from, [c_to]))

    problem = Problem("robot")
    problem.add_fluent(robot_at)
    problem.add_action(move)
    problem.add_object(c1)
    problem.add_object(c2)
    problem.add_object(r1)
    problem.set_initial_value(robot_at(r1, c1), True)
    problem.set_initial_value(robot_at(r1, c2), False)
    problem.add_goal(robot_at(r1, c2))

    motion_paths: Dict[MotionConstraint, Path] = {
        Waypoints(ObjectExp(r1), ObjectExp(c1), [ObjectExp(c2)]): ReedsSheppPath(
            [
                ((4.0, 26.0, -1.570796326794897), 0.0),
                ((4.024090241148528, 25.495925130590077, -1.5068310794722208), 0.0),
                ((4.0563552195272035, 24.992199074678314, -1.5068310794722208), 0.0),
                ((4.088620197905879, 24.488473018766552, -1.5068310794722208), 0.0),
                ((4.120885176284554, 23.98474696285479, -1.5068310794722208), 0.0),
                ((4.15315015466323, 23.481020906943026, -1.5068310794722208), 0.0),
                ((4.185415133041905, 22.977294851031264, -1.5068310794722208), 0.0),
                ((4.217680111420581, 22.473568795119505, -1.5068310794722208), 0.0),
                ((4.249945089799256, 21.969842739207742, -1.5068310794722208), 0.0),
                ((4.282210068177932, 21.46611668329598, -1.5068310794722208), 0.0),
                ((4.314475046556607, 20.962390627384217, -1.5068310794722208), 0.0),
                ((4.346740024935283, 20.458664571472454, -1.5068310794722208), 0.0),
                ((4.379005003313958, 19.95493851556069, -1.5068310794722208), 0.0),
                ((4.411269981692634, 19.45121245964893, -1.5068310794722208), 0.0),
                ((4.443534960071309, 18.947486403737166, -1.5068310794722208), 0.0),
                ((4.475799938449985, 18.443760347825403, -1.5068310794722208), 0.0),
                ((4.50806491682866, 17.94003429191364, -1.5068310794722208), 0.0),
                ((4.540329895207336, 17.436308236001878, -1.5068310794722208), 0.0),
                ((4.572594873586011, 16.93258218009012, -1.5068310794722208), 0.0),
                ((4.604859851964687, 16.428856124178356, -1.5068310794722208), 0.0),
                ((4.637124830343362, 15.925130068266593, -1.5068310794722208), 0.0),
                ((4.669389808722038, 15.42140401235483, -1.5068310794722208), 0.0),
                ((4.701654787100713, 14.917677956443068, -1.5068310794722208), 0.0),
                ((4.7339197654793885, 14.413951900531307, -1.5068310794722208), 0.0),
                ((4.766184743858064, 13.910225844619545, -1.5068310794722208), 0.0),
                ((4.7984497222367395, 13.406499788707784, -1.5068310794722208), 0.0),
                ((4.830714700615415, 12.902773732796021, -1.5068310794722208), 0.0),
                ((4.8629796789940904, 12.399047676884257, -1.5068310794722208), 0.0),
                ((4.895244657372766, 11.895321620972497, -1.5068310794722208), 0.0),
                ((4.927509635751441, 11.391595565060733, -1.5068310794722208), 0.0),
                ((4.959774614130117, 10.88786950914897, -1.5068310794722208), 0.0),
                ((4.992039592508792, 10.384143453237211, -1.5068310794722208), 0.0),
                ((5.024304570887468, 9.880417397325445, -1.5068310794722208), 0.0),
                ((5.056569549266143, 9.376691341413682, -1.5068310794722208), 0.0),
                ((5.088834527644819, 8.87296528550192, -1.5068310794722208), 0.0),
                ((5.121099506023494, 8.36923922959016, -1.5068310794722208), 0.0),
                ((5.15336448440217, 7.865513173678394, -1.5068310794722208), 0.0),
                ((5.185629462780845, 7.361787117766635, -1.5068310794722208), 0.0),
                ((5.217894441159521, 6.8580610618548725, -1.5068310794722208), 0.0),
                ((5.250159419538196, 6.35433500594311, -1.5068310794722208), 0.0),
                ((5.28389412984352, 5.850716451420794, -1.4796862055437154), 0.0),
                ((5.361370800830223, 5.352278468547841, -1.3534966239030854), 0.0),
                ((5.500962312965778, 4.867554560475057, -1.2273070422624555), 0.0),
                ((5.700448785554974, 4.4042531417727595, -1.1011174606218255), 0.0),
                ((5.95665784684912, 3.969741951780584, -0.9749278789811946), 0.0),
                ((6.26551508329395, 3.5709308877248027, -0.8487382973405646), 0.0),
                ((6.622108833669736, 3.214162118757322, -0.7225487156999346), 0.0),
                ((7.020768297722351, 2.9051092283988567, -0.5963591340593051), 0.0),
                ((7.453357036711573, 2.64960059460526, -0.4706734581230916), 0.0),
                ((7.914562785506687, 2.4503346007134454, -0.3449877821868781), 0.0),
                ((8.397109513815677, 2.310454887954066, -0.2193021062506646), 0.0),
                ((8.893384513814182, 2.232168213354619, -0.0936164303144511), 0.0),
                ((9.395558499023023, 2.2167096357090066, 0.03206924562176239), 0.0),
                ((9.89711361598862, 2.2506721872123165, 0.07491313757543272), 0.0),
                ((10.398446288798315, 2.288299004007954, 0.07491313757543272), 0.0),
                ((10.89977896160801, 2.325925820803591, 0.07491313757543272), 0.0),
                ((11.401111634417706, 2.3635526375992284, 0.07491313757543272), 0.0),
                ((11.902444307227402, 2.4011794543948657, 0.07491313757543272), 0.0),
                ((12.403776980037101, 2.4388062711905034, 0.07491313757543272), 0.0),
                ((12.905109652846793, 2.4764330879861403, 0.07491313757543272), 0.0),
                ((13.40644232565649, 2.514059904781778, 0.07491313757543272), 0.0),
                ((13.907774998466186, 2.551686721577415, 0.07491313757543272), 0.0),
                ((14.409107671275882, 2.5893135383730526, 0.07491313757543272), 0.0),
                ((14.910440344085577, 2.62694035516869, 0.07491313757543272), 0.0),
                ((15.411773016895275, 2.664567171964327, 0.07491313757543272), 0.0),
                ((15.91310568970497, 2.7021939887599644, 0.07491313757543272), 0.0),
                ((16.414438362514666, 2.7398208055556017, 0.07491313757543272), 0.0),
                ((16.91577103532436, 2.777447622351239, 0.07491313757543272), 0.0),
                ((17.417103708134057, 2.8150744391468763, 0.07491313757543272), 0.0),
                ((17.918436380943753, 2.852701255942514, 0.07491313757543272), 0.0),
                ((18.419769053753445, 2.890328072738151, 0.07491313757543272), 0.0),
                ((18.921101726563144, 2.9279548895337886, 0.07491313757543272), 0.0),
                ((19.42243439937284, 2.965581706329426, 0.07491313757543272), 0.0),
                ((19.923767072182535, 3.003208523125063, 0.07491313757543272), 0.0),
                ((20.42509974499223, 3.0408353399207004, 0.07491313757543272), 0.0),
                ((20.926432417801927, 3.0784621567163377, 0.07491313757543272), 0.0),
                ((21.427765090611622, 3.116088973511975, 0.07491313757543272), 0.0),
                ((21.92641067943828, 3.1777066741546727, 0.1847971581819653), 0.0),
                ((22.41349576278602, 3.30085617932413, 0.31048283411817923), 0.0),
                ((22.88130128351303, 3.4840928400137594, 0.4361685100543923), 0.0),
                ((23.322447092632714, 3.7245258954356304, 0.5618541859906058), 0.0),
                ((23.729973627566462, 4.018362248476311, 0.6875398619268193), 0.0),
                ((24.097451706933242, 4.3609663059949835, 0.8132255378630328), 0.0),
                ((24.419083957989738, 4.7469331104272925, 0.9389112137992461), 0.0),
                ((24.693484571891915, 5.176841593011522, 1.0665019086175291), 0.0),
                ((24.91095106144642, 5.638171546763291, 1.1940926034358121), 0.0),
                ((25.06794800597009, 6.123422986449974, 1.3216832982540951), 0.0),
                ((25.16192305707125, 6.624707027766175, 1.4492739930723784), 0.0),
                ((25.196118284431527, 7.13374772920208, 1.5280187951943522), 0.0),
                ((25.217943686481796, 7.6436436188626455, 1.5280187951943522), 0.0),
                ((25.23976908853206, 8.153539508523211, 1.5280187951943522), 0.0),
                ((25.261594490582326, 8.663435398183777, 1.5280187951943522), 0.0),
                ((25.283419892632594, 9.173331287844343, 1.5280187951943522), 0.0),
                ((25.30524529468286, 9.683227177504909, 1.5280187951943522), 0.0),
                ((25.327070696733124, 10.193123067165475, 1.5280187951943522), 0.0),
                ((25.348896098783392, 10.70301895682604, 1.5280187951943522), 0.0),
                ((25.370721500833657, 11.212914846486607, 1.5280187951943522), 0.0),
                ((25.392546902883925, 11.722810736147173, 1.5280187951943522), 0.0),
                ((25.41437230493419, 12.232706625807738, 1.5280187951943522), 0.0),
                ((25.436197706984455, 12.742602515468304, 1.5280187951943522), 0.0),
                ((25.458023109034723, 13.25249840512887, 1.5280187951943522), 0.0),
                ((25.479848511084988, 13.762394294789436, 1.5280187951943522), 0.0),
                ((25.501673913135257, 14.272290184450002, 1.5280187951943522), 0.0),
                ((25.52349931518552, 14.782186074110568, 1.5280187951943522), 0.0),
                ((25.545324717235786, 15.292081963771134, 1.5280187951943522), 0.0),
                ((25.567150119286055, 15.8019778534317, 1.5280187951943522), 0.0),
                ((25.58897552133632, 16.311873743092264, 1.5280187951943522), 0.0),
                ((25.610800923386588, 16.82176963275283, 1.5280187951943522), 0.0),
                ((25.632626325436853, 17.331665522413395, 1.5280187951943522), 0.0),
                ((25.654451727487118, 17.84156141207396, 1.5280187951943522), 0.0),
                ((25.676277129537386, 18.351457301734527, 1.5280187951943522), 0.0),
                ((25.69810253158765, 18.861353191395093, 1.5280187951943522), 0.0),
                ((25.71992793363792, 19.37124908105566, 1.5280187951943522), 0.0),
                ((25.741753335688184, 19.881144970716228, 1.5280187951943522), 0.0),
                ((25.76357873773845, 20.39104086037679, 1.5280187951943522), 0.0),
                ((25.785404139788717, 20.90093675003736, 1.5280187951943522), 0.0),
                ((25.807229541838982, 21.410832639697922, 1.5280187951943522), 0.0),
                ((25.829054943889247, 21.92072852935849, 1.5280187951943522), 0.0),
                ((25.850880345939515, 22.430624419019058, 1.5280187951943522), 0.0),
                ((25.87270574798978, 22.940520308679623, 1.5280187951943522), 0.0),
                ((25.89453115004005, 23.45041619834019, 1.5280187951943522), 0.0),
                ((25.916356552090313, 23.96031208800075, 1.5280187951943522), 0.0),
                ((25.938181954140582, 24.470207977661325, 1.5280187951943522), 0.0),
                ((25.960007356190847, 24.980103867321887, 1.5280187951943522), 0.0),
                ((25.98183275824111, 25.489999756982453, 1.5280187951943522), 0.0),
                ((26.0, 26.0, 1.5707963267948966), 0.0),
            ]
        )
    }

    plan = up.plans.SequentialPlan([move(r1, c1, c2, motion_paths=motion_paths)])

    tamp_feasible = Example(problem=problem, plan=plan)
    problems["tamp_feasible"] = tamp_feasible

    return problems
