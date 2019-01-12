import enum


class Role(enum.Enum):

    @classmethod
    def to_choices(cls):
        return [(role.value, role.name) for role in cls]

    USER = 1
    MODERATOR = 2
    ADMIN = 3
    DEVELOPER = 4


class Course(enum.Enum):

    @classmethod
    def to_choices(cls):
        return [(course.value, '{0} - {1}'.format(course.name, course.value)) for course in cls]

    CS100 = 'Discovering Computer Science'
    CS107 = 'Introduction to Computing and Programming'
    CS109 = 'C/C ++ Programming for Engineers with MatLab'
    CS110 = 'MATLAB Programming for Engineers'
    CS111 = 'Program Design I'
    CS141 = 'Program Design II'
    CS151 = 'Mathematical Foundations of Computing'
    CS201 = 'Data Structures and Discrete Mathematics I'
    CS211 = 'Programming Practicum'
    CS251 = 'Data Structures'
    CS261 = 'Machine Organization'
    CS301 = 'Languages and Automata'
    CS341 = 'Programming Language Design and Implementation.'
    CS342 = 'Software Design'
    CS361 = 'Systems Programming'
    CS362 = 'Computer Design'
    CS377 = 'Communication and Ethical Issues in Computing'
    CS398 = 'Undergraduate Design/Research'
    CS401 = 'Computer Algorithms I'
    CS411 = 'Artificial Intelligence I'
    CS412 = 'Introduction to Machine Learning'
    CS415 = 'Computer Vision I'
    CS418 = 'Introduction to Data Science'
    CS421 = 'Natural Language Processing'
    CS422 = 'User Interface Design and Programming'
    CS424 = 'Visualization and Visual Analytics'
    CS425 = 'Computer Graphics I'
    CS426 = 'Video Game Design and Development'
    CS428 = 'Virtual, Augmented and Mixed Reality'
    CS440 = 'Software Engineering I'
    CS441 = 'Engineering Distributed Objects For Cloud Computing'
    CS442 = 'Software Engineering II'
    CS450 = 'Introduction to Networking'
    CS455 = 'Design and Implementation of Network Protocols'
    CS461 = 'Operating Systems Design and Implementation'
    CS466 = 'Advanced Computer Architecture'
    CS469 = 'Hardware Description Language Based Digital and Computer System Design'
    CS473 = 'Compiler Design'
    CS474 = 'Object-Oriented Languages and Environments'
    CS475 = 'Object-Oriented Programming'
    CS476 = 'Programming Language Design'
    CS477 = 'Public Policy, Legal, and Ethical Issues in Computing, Privacy, and Security'
    CS478 = 'Software Development for Mobile Platforms'
    CS480 = 'Database Systems'
    CS485 = 'Networked Operating Systems Programming'
    CS486 = 'Secure Operating System Design and Implementation'
    CS487 = 'Building Secure Computer Systems'
    CS489 = 'Human Augmentics'
    CS501 = 'Computer Algorithms II'
    CS502 = 'Design and Analysis of Efficient Algorithms in Computational Molecular Biology'
    CS503 = 'Applied Graph Theory'
    CS505 = 'Computability and Complexity Theory'
    CS506 = 'An Introduction to Quantum Computing'
    CS510 = 'Introduction to Cognitive Science'
    CS511 = 'Artificial Intelligence II'
    CS512 = 'Advanced Machine Learning'
    CS514 = 'Applied Artificial Intelligence'
    CS515 = 'Advanced Computer Vision'
    CS521 = 'Statistical Natural Language Processing'
    CS522 = 'Human-Computer Interaction'
    CS523 = 'Multi-Media Systems'
    CS524 = 'Visualization and Visual Analytics II'
    CS525 = 'Advanced Graphics Processor Programming'
    CS526 = 'Computer Graphics II'
    CS527 = 'Computer Animation'
    CS528 = 'Virtual Reality'
    CS540 = 'Advanced Topics in Software Engineering'
    CS541 = 'Software Engineering Environments'
    CS542 = 'Distributed Software Engineering'
    CS545 = 'Formal Methods In Concurrent and Distributed Systems'
    CS550 = 'Advanced Computer Networks'
    CS553 = 'Distributed Computing Systems'
    CS554 = 'Advanced Topics in Concurrent Computing Systems'
    CS559 = 'Neural Networks'
    CS560 = 'Fuzzy Logic'
    CS565 = 'Physical Design Automation'
    CS566 = 'Parallel Processing'
    CS567 = 'Principles of Computational Transportation Science'
    CS569 = 'High-Performance Processors and Systems'
    CS577 = 'Object Stores'
    CS580 = 'Query Processing in Database Systems'
    CS581 = 'Database Management Systems'
    CS582 = 'Information Retrieval'
    CS583 = 'Data Mining and Text Mining'
    CS584 = 'Advanced Data Mining'
    CS586 = 'Data and Web Semantics'
    CS587 = 'Computer Systems Security'
    CS588 = 'Security and Privacy in Networked and Distributed Systems'
    CS590 = 'Research Methods in Computer Science'


class Skill(enum.Enum):

    @classmethod
    def to_choices(cls):
        return [(skill.value, skill.value) for skill in cls]

    HTML = 'HTML'
    CSS = 'CSS'
    BOOTSTRAP = 'Bootstrap'
    JAVASCRIPT = 'Javascript'
    ANGULARJS = 'AngularJS'
    JQUERY = 'jQuery'
    REACT = 'React'
    NODEJS = 'Node.js'
    IOS_DEV = 'iOS Dev'
    ANDROID_DEV = 'Android Dev'
    PYTHON = 'Python'
    DJANGO = 'Django'
    FLASK = 'Flask'
    C = 'C'
    CPP = 'C++'
    C_SHARP = 'C#'
    JAVA = 'Java'
    PHP = 'PHP'
    RUBY = 'Ruby'
    RAILS = 'Rails'
    PERL = 'Perl'
    SQL = 'SQL'
    NOSQL = 'NoSQL'
    MONGODB = 'MongoDB'
    GIT = 'Git'
    PHOTOSHOP = 'Photoshop'
    ILLUSTRATOR = 'Illustrator'
    LINUX = 'Linux'
