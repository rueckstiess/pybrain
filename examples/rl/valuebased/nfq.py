__author__ = 'Thomas Rueckstiess, ruecksti@in.tum.de'

from pybrain.rl.environments.cartpole import CartPoleEnvironment, DiscreteBalanceTask, DiscreteJustBalanceTask, CartPoleRenderer
from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import EpisodicExperiment
from pybrain.rl.learners.valuebased import NFQ, ActionValueNetwork

from numpy import array, arange, meshgrid, pi, ones, zeros, mean, random
from matplotlib import pyplot as plt
from copy import deepcopy

# switch this to True if you want to see the cart balancing the pole (slower)
render = False

plt.ion()

env = CartPoleEnvironment()
if render:
    renderer = CartPoleRenderer()
    env.setRenderer(renderer)
    renderer.start()

module = ActionValueNetwork(4, 3)

task = DiscreteJustBalanceTask(env, 200)
learner = NFQ(maxEpochs=50)
learner.explorer.epsilon = 0.3
learner.explorer.decay = 0.999

agent = LearningAgent(module, learner)
testagent = LearningAgent(module, None)
experiment = EpisodicExperiment(task, agent)

def plotPerformance(values, fig):
    plt.figure(fig.number)
    plt.clf()
    plt.plot(values, 'o-')
    plt.gcf().canvas.draw()

performance = []

if not render:
    pf_fig = plt.figure()

while(True):
	# one learning step after one episode of world-interaction
    experiment.doEpisodes(1)    
    agent.learn(1)
    
    while agent.history.getNumSequences() > 50:
        agent.history.removeSequence(0)
    
    # test performance (these real-world experiences are not used for training)
    if render:
        env.delay = True
    experiment.agent = testagent
    r = mean([sum(x) for x in experiment.doEpisodes(25)])
    env.delay = False
    testagent.reset()
    experiment.agent = agent
    
    performance.append(r)
    if not render:
        plotPerformance(performance, pf_fig)
    
    print "reward avg", r
    print "explorer epsilon", learner.explorer.epsilon
    print "num episodes", agent.history.getNumSequences()
    print "update step", len(performance)
    print "dataset length", len(agent.history)
    print "-------------------------------"
    
