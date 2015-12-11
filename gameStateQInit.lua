os.execute("rm qlearning/trainingRecord.csv")
os.execute("rm qlearning/test.dat")
Brain = require 'deepqlearn'
Brain.init(16, 4)
torch.save("qlearning/test.dat", Brain)
i = 0
torch.save("qlearning/test_iter.dat", i)