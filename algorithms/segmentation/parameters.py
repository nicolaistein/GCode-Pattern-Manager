# ------- Features

# Max length of DFS result when extending features
max_string_length: int = 5

# minimum feature length
min_feature_length: int = 15

# percentage of edges that are used for feature generation
featureCountPercentage = 0.05

tao = 16

featureNeighborLevel = 1

# ------- Charts

epsilonFactor = 1 / 3.5

# The minimum distance to a feature a face must have in order to
seedMinFeatureDistance = 2

# The fraction of total faces a chart has to contain in order not to
# be "deleted"
# Old: 1/45
# Best:1/25
minChartSizeFactor = 1 / 50

featureBarrier = True

expandingUntilFeatureDistance = 1

maxSOD = 10

mergingUpToSOD = 14

# Absolute count of seeds used for chart generation
localMaximumSeedCount = 500000

globalMaximumSeedCount = 0
