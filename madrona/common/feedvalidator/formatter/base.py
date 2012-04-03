"""$Id: base.py 1055 2009-05-19 15:12:42Z sa3ruby $"""

__author__ = "Sam Ruby <http://intertwingly.net/> and Mark Pilgrim <http://diveintomark.org/>"
__version__ = "$Revision: 1055 $"
__copyright__ = "Copyright (c) 2002 Sam Ruby and Mark Pilgrim"

"""Base class for output classes"""

from UserList import UserList
import os
LANGUAGE = os.environ.get('LANGUAGE', 'en')
lang = __import__('madrona.common.feedvalidator.i18n.%s' % LANGUAGE, globals(), locals(), LANGUAGE)

from madrona.common.feedvalidator.logging import Info, Warning, Error

class BaseFormatter(UserList):
  def __getitem__(self, i):
    return self.format(self.data[i])

  def getErrors(self):
    return [self.format(msg) for msg in self.data if isinstance(msg,Error)]

  def getWarnings(self):
    return [self.format(msg) for msg in self.data if isinstance(msg,Warning)]

  def getLine(self, event):
    if not event.params.has_key('line'): return ''
    return lang.line % event.params

  def getColumn(self, event):
    if not event.params.has_key('column'): return ''
    return lang.column % event.params

  def getLineAndColumn(self, event):
    line = self.getLine(event)
    if not line: return ''
    column = self.getColumn(event)
    return '%s, %s:' % (line, column)
  
  def getCount(self, event):
    if not event.params.has_key('msgcount'): return ''
    count = int(event.params['msgcount'])
    if count <= 1: return ''
    return lang.occurances % event.params
  
  def getMessageClass(self, event):
    classes = [event.__class__]
    while len(classes):
      if lang.messages.has_key(classes[0]):
        return classes[0]
      classes = classes + list(classes[0].__bases__)
      del classes[0]
    return "Undefined message: %s[%s]" % (event.__class__, event.params)
    
  def getMessage(self, event):
    classes = [event.__class__]
    while len(classes):
      if lang.messages.has_key(classes[0]):
        try:
          return lang.messages[classes[0]] % event.params
        except:
          return lang.messages[classes[0]] + ' % ' + repr(event.params)
      classes = classes + list(classes[0].__bases__)
      del classes[0]
    return "Undefined message: %s[%s]" % (event.__class__, event.params)
    
  def format(self, event):
    """returns the formatted representation of a single event"""
    return `event`