----------------------------------------------------------------------
-- This script shows how to train different models on the MNIST 
-- dataset, using multiple optimization techniques (SGD, LBFGS)
--
-- This script demonstrates a classical example of training 
-- well-known models (convnet, MLP, logistic regression)
-- on a 10-class classification problem. 
--
-- It illustrates several points:
-- 1/ description of the model
-- 2/ choice of a loss function (criterion) to minimize
-- 3/ creation of a dataset as a simple Lua table
-- 4/ description of training and test procedures
--
-- Clement Farabet
----------------------------------------------------------------------

require 'torch'
require 'nn'
require 'nnx'
require 'optim'
require 'image'
require 'dataset-mnist'
require 'pl'
require 'paths'
require 'rnn'
require 'gnuplot'

----------------------------------------------------------------------

-- fix seed
torch.manualSeed(1)

-- threads
torch.setnumthreads(4)
print('<torch> set nb of threads to ' .. torch.getnumthreads())

-- use floats, for SGD

-- torch.setdefaulttensortype('torch.LongTensor')


----------------------------------------------------------------------
-- define model to train
-- on the 10-class classification problem
--
-- file = io.open('/home/hexu/mobile-data/datamanaging/99070810115182195_stations.txt','r')
-- classes = {}
-- num = 1
-- for line in file:lines() do 
--    classes[num] = line
--    num = num + 1
-- end
-- file.close()
classes = {1,2,3,4,5,6}


-- rho = 100
-- hiddenSize = 10
-- r = nn.Recurrent(
--     hiddenSize, nn.Linear(3,hiddenSize),
--     nn.Linear(hiddenSize, hiddenSize), nn.Tanh(),
--     rho)

-- h = nn.Recurrent(
--     hiddenSize, nn.Linear(hiddenSize,hiddenSize),
--     nn.Linear(hiddenSize, hiddenSize), nn.Tanh(),
--     rho)

model = nn.Sequential()
model:add(nn.Linear(7,10))
model:add(nn.ReLU())
model:add(nn.Linear(10,10))
model:add(nn.ReLU())
model:add(nn.Linear(10,10))
model:add(nn.ReLU())
model:add(nn.Linear(10,10))
model:add(nn.ReLU())
model:add(nn.Linear(10,#classes))




-- retrieve parameters and gradients
parameters,gradParameters = model:getParameters()

----------------------------------------------------------------------
-- loss function: negative log-likelihood
--
model:add(nn.LogSoftMax())
criterion = nn.ClassNLLCriterion()

----------------------------------------------------------------------
-- get/create dataset
--
function split(str, delimiter)
    if str==nil or str=='' or delimiter==nil then
        return nil
    end
    
    local result = {}
    for match in (str..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match)
    end
    return result
end

function fileio(filename,m,n)
    local file = io.open(filename,'r')
    ls = torch.Tensor(m,n)
    i = 0
    for line in file:lines() do
        i = i + 1
        list = split(line,' ')
        for j=1,n do
            ls[i][j] = list[j]
        end
    end
    return ls
end

-- train_dataset = fileio('/home/hexu/mobile-data/new_data/singleUser/99070810242857078_finaldata.txt',99337,8)  
train_dataset = fileio('/home/hexu/mobile-data/24time_finaldata/7_24traindata.txt', 15000000,8)  
test_dataset = fileio('/home/hexu/mobile-data/24time_finaldata/7_24testdata.txt',4000000,8) 
-- test_dataset = fileio('/home/hexu/mobile-data/new_data/singleUser/99070866254051654_finaldata.txt',52797,8) 

-- create training set and normalize


----------------------------------------------------------------------
-- define training and testing functions
--

-- this matrix records the current confusion across classes
confusion = optim.ConfusionMatrix(classes) 

-- log results to files
trainLogger = optim.Logger(paths.concat('/home/hexu/mobile-data/logs', '7_24time_train.log'))
testLogger = optim.Logger(paths.concat('/home/hexu/mobile-data/logs', '7_24time_test.log'))

 batchSize = 10000
-- training function
function train(dataset)
   -- epoch tracker
   epoch = epoch or 1
   local trainSetSize = 15000000
  
   -- local vars
   local time = sys.clock()

   -- do one epoch
   print('<trainer> on training set:')
   print("<trainer> online epoch # " .. epoch .. ' [batchSize = ' .. batchSize .. ']')
   for t = 1,trainSetSize,batchSize do
      -- create mini batch
      local inputs = torch.Tensor(batchSize,7)
      local targets = torch.Tensor(batchSize)
      local k = 1
      for i = t,math.min(t+batchSize-1,trainSetSize) do
         -- load new sample
         local sample = dataset[i]
         local input = sample:sub(1,7):clone()
         local result = torch.Tensor(6):zero()
         for j = 1,6 do
            if sample[8] == j then
               result[j] = 1 
            end
         end

         -- print(result)
         local _,target = result:clone():max(1)
         target = target:squeeze()
         -- print(target)
         inputs[k] = input
         targets[k] = target
         k = k + 1
      end

      -- create closure to evaluate f(X) and df/dX
      local feval = function(x)
         -- just in case:
         collectgarbage()

         -- get new parameters
         if x ~= parameters then
            parameters:copy(x)
         end

         -- reset gradients
         gradParameters:zero()

         -- evaluate function for complete mini batch
         local outputs = model:forward(inputs)
         -- print(outputs)
         local f = criterion:forward(outputs, targets)

         -- estimate df/dW
         local df_do = criterion:backward(outputs, targets)
         model:backward(inputs, df_do)

         -- penalties (L1 and L2):
         -- if opt.coefL1 ~= 0 or opt.coefL2 ~= 0 then
         --    -- locals:
         --    local norm,sign= torch.norm,torch.sign

         --    -- Loss:
         --    f = f + opt.coefL1 * norm(parameters,1)
         --    f = f + opt.coefL2 * norm(parameters,2)^2/2

         --    -- Gradients:
         --    gradParameters:add( sign(parameters):mul(opt.coefL1) + parameters:clone():mul(opt.coefL2) )
         -- end

         -- update confusion
         for i = 1,batchSize do
            confusion:add(outputs[i], targets[i])
         end

         -- return f and df/dX
         return f,gradParameters
      end
      
      -- optimize on current mini-batch


      -- Perform SGD step:
      sgdState = sgdState or {
         learningRate = 0.01,
         momentum = 0,
         learningRateDecay = 5e-7
      }

      optim.sgd(feval, parameters, sgdState)
      -- disp progress
      xlua.progress(t, trainSetSize)
   end


   -- time taken
   time = sys.clock() - time
   time = time / trainSetSize
   print("<trainer> time to learn 1 sample = " .. (time*1000) .. 'ms')

   -- print confusion matrix
   print(confusion)
   trainLogger:add{['% mean class accuracy (train set)'] = confusion.totalValid * 100}
   confusion:zero()

   -- save/log current net
   local filename = paths.concat('/usr/local/trajectory-prediction/tralogs', 'tra.net')
   os.execute('mkdir -p ' .. sys.dirname(filename))
   if paths.filep(filename) then
      os.execute('mv ' .. filename .. ' ' .. filename .. '.old')
   end
   print('<trainer> saving network to '..filename)
   -- torch.save(filename, model)

   -- next epoch
   epoch = epoch + 1
end

-- test function
function test(dataset)
   flag = flag or 1
   -- local vars
   local time = sys.clock()
   local testSetSize = 4000000
   -- test over given dataset
   print('<trainer> on testing Set:')
   for t = 1,testSetSize,batchSize do
      -- disp progress
      xlua.progress(t, testSetSize)

      -- create mini batch
      local inputs = torch.Tensor(batchSize,7)
      local targets = torch.Tensor(batchSize)
      local k = 1
      for i = t,math.min(t+batchSize-1,testSetSize) do
         -- load new sample
         local sample = dataset[i]
         local input = sample:sub(1,7):clone()
         local result = torch.Tensor(6):zero()
         for j = 1,6 do
            if sample[8] == j then
               result[j] = 1
            end
         end
         -- print(sample[3])
         local _,target = result:clone():max(1)
         target = target:squeeze()
         inputs[k] = input
         targets[k] = target
         k = k + 1
      end

      -- test samples
      local preds = model:forward(inputs)

      -- confusion:
      for i = 1,batchSize do
         confusion:add(preds[i], targets[i])
      end

-- 在最后一个迭代期将预测数据与实际数据写入文件以便观察
      -- if flag == 30 then
      --   local file = io.open('/home/hexu/mobile-data/new_data/result/LUtargets.txt','a+')
      --   local file2 = io.open('/home/hexu/mobile-data/new_data/result/LUpreds.txt','a+')
      --   for i = 1, batchSize do
      --     file:write(tostring(targets[i]))
      --     file:write('\n')
      --     local _,pred = preds[i]:clone():max(1)
      --     pred = pred:squeeze()
      --     file2:write(tostring(pred))
      --     file2:write('\n')
      --   end
      --   file:close()
      --   file2:close()
      -- end


   end


   -- timing
   time = sys.clock() - time
   time = time / testSetSize
   print("<trainer> time to test 1 sample = " .. (time*1000) .. 'ms')

   -- print confusion matrix
   print(confusion)
   testLogger:add{['% mean class accuracy (test set)'] = confusion.totalValid * 100}
   confusion:zero()

   flag = flag + 1
end

----------------------------------------------------------------------
-- and train!
--
for i =1,30 do
   -- train/test
   train(train_dataset)
   test(test_dataset)

   -- plot errors
   trainLogger:style{['% mean class accuracy (train set)'] = '-'}
   testLogger:style{['% mean class accuracy (test set)'] = '-'}
   trainLogger:plot()
   testLogger:plot()
end

-- torch.save('/home/hexu/mobile-data/new_data/model/2000LU_model2.lua',model)


