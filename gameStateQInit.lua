Brain = require 'deepqlearn'
Brain.init(16, 4)
torch.save("test.dat", Brain)
i = 0
torch.save("test_iter.dat", i)