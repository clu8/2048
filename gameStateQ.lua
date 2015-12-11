-- Brain = require 'deepqlearn'
require 'deepqlearn'
Brain = torch.load("qlearning/test.dat")
last_index = torch.load("qlearning/test_iter.dat")

function string:split( inSplitPattern, outResults )
   if not outResults then
      outResults = {}
   end
   local theStart = 1
   local theSplitStart, theSplitEnd = string.find( self, inSplitPattern, theStart )
   while theSplitStart do
      table.insert( outResults, string.sub( self, theStart, theSplitStart-1 ) )
      theStart = theSplitEnd + 1
      theSplitStart, theSplitEnd = string.find( self, inSplitPattern, theStart )
   end
   table.insert( outResults, string.sub( self, theStart ) )
   return outResults
end

-- Brain.init(16, 4)
for i = last_index, last_index + 10000000 do
	state = io.read()
	t = state:split(" ")
	reward = t[17]
	max_score = t[18]
	t[17] = nil
	t[18] = nil
	t[19] = nil
	if i % 10240 == 0 then
		torch.save("qlearning/test_iter.dat", i)
		meta_output = io.open("qlearning/training_meta.txt", "w")
		meta_output:write("training number: ", i, "\nmax score: ", max_score)
		meta_output:close()
	end
	if i % 102400 == 0 then
		torch.save("qlearning/test.dat", Brain)
	end
	-- print table
	-- print(state)
	Brain.backward(reward)
	action = Brain.forward(t)
	print(action - 1)
end