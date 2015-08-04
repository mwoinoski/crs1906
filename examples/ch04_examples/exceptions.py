from collections import namedtuple

try:
    elements = {'H': 'hydrogen', 'He': 'Helium'}
    print(elements['Li'])
except KeyError as ke:
    print('Error accessing item', ke)
finally:
    print('Done with elements')

class TicketException(Exception):
    pass

Ticket = namedtuple('Ticket', 'event_name date_time price')

def process_ticket(ticket):
    if not ticket.date_time:
        raise TicketException('No date/time for event',
                              ticket.event_name)

try:
    t = Ticket('XKCD Con', None, 1000.0)
    process_ticket(t)
    print('Ticket {} is ok'.format(t))
except TicketException as te:
    print(te.args)

try:
    f = open('/crs1906/index.html')
    for line in f:
        print(line, end="")
finally:
    try:
        f.close()  # if open() fails, f doesn't exist
    except NameError:
        pass

with open('/crs1906/index.html') as f:
    for line in f:
        print(line, end="")
