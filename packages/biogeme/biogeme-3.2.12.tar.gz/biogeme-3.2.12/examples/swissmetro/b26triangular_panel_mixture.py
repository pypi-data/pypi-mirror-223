"""File b26triangular_panel_mixture.py

:author: Michel Bierlaire, EPFL
:date: Tue Dec  6 18:30:44 2022

 Example of a mixture of logit models, using Monte-Carlo integration.
 THe micing distribution is user-defined (triangular, here).
 The datafile is organized as panel data.
"""
import numpy as np
import biogeme.biogeme as bio
from biogeme import models
import biogeme.logging as blog
from biogeme.expressions import (
    Beta,
    bioDraws,
    MonteCarlo,
    PanelLikelihoodTrajectory,
    log,
)

from swissmetro_panel import (
    database,
    CHOICE,
    CAR_AV_SP,
    TRAIN_AV_SP,
    TRAIN_TT_SCALED,
    TRAIN_COST_SCALED,
    SM_TT_SCALED,
    SM_COST_SCALED,
    CAR_TT_SCALED,
    CAR_CO_SCALED,
    SM_AV,
)

logger = blog.get_screen_logger(level=blog.INFO)
logger.info('Example b26triangular_panel_mixture.py')


def the_triangular_generator(sample_size, number_of_draws):
    """
    Provide my own random number generator to the database.
    See the numpy.random documentation to obtain a list of other distributions.
    """
    return np.random.triangular(-1, 0, 1, (sample_size, number_of_draws))


myRandomNumberGenerators = {
    'TRIANGULAR': (
        the_triangular_generator,
        'Draws from a triangular distribution',
    )
}
database.setRandomNumberGenerators(myRandomNumberGenerators)

# Parameters to be estimated
B_COST = Beta('B_COST', 0, None, None, 0)

# Define a random parameter, normally distributed across individuals,
# designed to be used for Monte-Carlo simulation
B_TIME = Beta('B_TIME', 0, None, None, 0)

# It is advised not to use 0 as starting value for the following parameter.
B_TIME_S = Beta('B_TIME_S', 1, None, None, 0)
B_TIME_RND = B_TIME + B_TIME_S * bioDraws('B_TIME_RND', 'TRIANGULAR')

# We do the same for the constants, to address serial correlation.
ASC_CAR = Beta('ASC_CAR', 0, None, None, 0)
ASC_CAR_S = Beta('ASC_CAR_S', 1, None, None, 0)
ASC_CAR_RND = ASC_CAR + ASC_CAR_S * bioDraws('ASC_CAR_RND', 'TRIANGULAR')

ASC_TRAIN = Beta('ASC_TRAIN', 0, None, None, 0)
ASC_TRAIN_S = Beta('ASC_TRAIN_S', 1, None, None, 0)
ASC_TRAIN_RND = ASC_TRAIN + ASC_TRAIN_S * bioDraws('ASC_TRAIN_RND', 'TRIANGULAR')

ASC_SM = Beta('ASC_SM', 0, None, None, 1)
ASC_SM_S = Beta('ASC_SM_S', 1, None, None, 0)
ASC_SM_RND = ASC_SM + ASC_SM_S * bioDraws('ASC_SM_RND', 'TRIANGULAR')

# Definition of the utility functions
V1 = ASC_TRAIN_RND + B_TIME_RND * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED
V2 = ASC_SM_RND + B_TIME_RND * SM_TT_SCALED + B_COST * SM_COST_SCALED
V3 = ASC_CAR_RND + B_TIME_RND * CAR_TT_SCALED + B_COST * CAR_CO_SCALED

# Associate utility functions with the numbering of alternatives
V = {1: V1, 2: V2, 3: V3}

# Associate the availability conditions with the alternatives
av = {1: TRAIN_AV_SP, 2: SM_AV, 3: CAR_AV_SP}

# Conditional to the random parameters, the likelihood of one observation is
# given by the logit model (called the kernel)
obsprob = models.logit(V, av, CHOICE)

# Conditional to the random parameters, the likelihood of all observations for
# one individual (the trajectory) is the product of the likelihood of
# each observation.
condprobIndiv = PanelLikelihoodTrajectory(obsprob)

# We integrate over the random parameters using Monte-Carlo
logprob = log(MonteCarlo(condprobIndiv))

# Create the Biogeme object
the_biogeme = bio.BIOGEME(database, logprob)
the_biogeme.modelName = 'b26triangular_panel_mixture'

# Estimate the parameters.
results = the_biogeme.estimate()
print(results.short_summary())
pandas_results = results.getEstimatedParameters()
print(pandas_results)
