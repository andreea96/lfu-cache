table = {}
lfu = None


class ValueNode:

  def __init__(self, nextVal, freqNode, val, prevVal=None):
    self.nextVal = nextVal
    self.freqNode = freqNode
    self.val = val
    self.prevVal = prevVal


class FreqNode:
  def __init__(self, nextFreqNode, freq, last=None):
    self.nextFreqNode = nextFreqNode
    self.freq = freq
    self.last = last


def add(key, value):
  global lfu
  global table
  valNode = None
  if lfu is None:
    freqNode = FreqNode(None, 1)
    valNode = ValueNode(None, freqNode, value)
    lfu = freqNode
    freqNode.last = valNode
  elif lfu.freq == 1:
    valNode = ValueNode(None, lfu, value, lfu.last)
    lfu.last = valNode
  else:
    new_root = FreqNode(lfu, 1)
    lfu = new_root
    valNode = ValueNode(None, lfu, value)
    lfu.last = valNode
  table[key] = valNode
  

def get(key):
  global lfu
  global table
  valNode = table[key]
  if valNode is None:
    raise Exception
  if valNode.freqNode.nextFreqNode is None:
    # new freq node
    new_freq_node = FreqNode(valNode.freqNode.nextFreqNode, valNode.freqNode.freq + 1)
    valNode.freqNode.nextFreqNode = new_freq_node
  # print(valNode.freqNode.freq, valNode.freqNode.nextFreqNode.freq)
  if valNode.freqNode.freq + 1 == valNode.freqNode.nextFreqNode.freq:
    oldFreqMaster = valNode.freqNode
    newFreqMaster = valNode.freqNode.nextFreqNode
    oldPrevValue = valNode.prevVal
    oldNextValue = valNode.nextVal
    # break old val links
    if oldPrevValue is not None:
      oldPrevValue.nextVal = oldNextValue
    if oldNextValue is not None:
      oldNextValue.prevVal = oldPrevValue
    # build new val links
    valNode.prevVal = newFreqMaster.last
    valNode.nextVal = None
    if oldNextValue is None:
      oldFreqMaster.last = None
    elif oldPrevValue is not None:
      oldFreqMaster.last = oldPrevValue
    else:
      #nodul trebuie sters
      if lfu == oldFreqMaster:
        lfu = oldFreqMaster.nextFreqNode
        del oldFreqMaster
    valNode.freqNode = newFreqMaster

def evict(): 
  global lfu
  global table
  if lfu is None:
    return
  oldLast = lfu.last
  if oldLast.prevVal == None:
    #it had only one value, the freq node can be deleted
    oldLfu = lfu
    lfu = lfu.nextFreqNode
    del oldLfu
    del oldLast
  else: 
    lfu.last = oldLast.prevVal
    del oldLast

  
add(1, 3)  #v1
add(2, 2)  #v2
# add(3, 1)
get(2)
# evict()
# evict()
print(lfu.last.val)
print(table[1])


