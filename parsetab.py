
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'WORDtext : wordswords : words WORD\n             | WORD'
    
_lr_action_items = {'WORD':([0,2,3,4,],[3,4,-3,-2,]),'$end':([1,2,3,4,],[0,-1,-3,-2,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'text':([0,],[1,]),'words':([0,],[2,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> text","S'",1,None,None,None),
  ('text -> words','text',1,'p_text','AyaDictionnary.py',87),
  ('words -> words WORD','words',2,'p_words','AyaDictionnary.py',92),
  ('words -> WORD','words',1,'p_words','AyaDictionnary.py',93),
]
