from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()


class Table(base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDo:

    def __init__(self):
        self.session: None = None
        self.init_db()
        self.today: datetime.date = datetime.today().date()
        self.actions: dict = {'1': self.today_tasks,
                              '2': self.week_tasks,
                              '3': self.all_tasks,
                              '4': self.missed_tasks,
                              '5': self.create_task,
                              '6': self.delete_task,
                              '0': exit}

    def init_db(self):
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def create_task(self):
        task, deadline = input('Enter task:\n'), input('Enter deadline:\n')
        new_row = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')

    def today_tasks(self):
        tasks = self.session.query(Table).filter(Table.deadline == self.today).all()
        print(f'\nToday {datetime.today().day} {datetime.today().strftime("%b")}:')
        if not tasks:
            print('Nothing to do!')
        else:
            for i, todo in enumerate(tasks, 1):
                print(f'{i}. {todo}')

    def week_tasks(self):
        for day in [self.today + timedelta(days=x) for x in range(7)]:
            tasks = self.session.query(Table).filter(Table.deadline == day).all()
            print(f"\n{day.strftime('%A %-d %b:')}")
            if tasks:
                for x, todo in enumerate(tasks, 1):
                    print(f'{x}. {todo}')
            else:
                print('Nothing to do!\n')

    def all_tasks(self):
        tasks = self.session.query(Table).filter(Table.deadline).order_by(Table.deadline).all()
        print('\nAll tasks:')
        for i, todo in enumerate(tasks, 1):
            print(f'{i}. {todo}. {todo.deadline.strftime("%-d %b")}')

    def missed_tasks(self):
        tasks = self.session.query(Table).filter(Table.deadline < self.today).all()
        print('Missed tasks:')
        if tasks:
            for x, todo in enumerate(tasks, 1):
                print(f'{x}. {todo}. {todo.deadline.strftime("%-d %b")}')
        else:
            print('Nothing is missed!')

    def delete_task(self):
        rows = self.session.query(Table).filter(Table.deadline).all()
        if rows:
            for x, todelete in enumerate(rows, 1):
                print(f'{x}. {todelete}. {todelete.deadline.strftime("%-d %b")}')
            choice = input()
            self.session.delete(rows[int(choice) - 1])
            self.session.commit()
            print('The task has been deleted!')
            return
        print('Nothing to delete')
        return

    def menu(self):
        while True:
            print()
            choice: str = input('1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks\n'
                                '4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n')
            if choice in self.actions:
                self.actions[choice]()
            else:
                print('Unknown option.')


if __name__ == "__main__":
    ToDo().menu()
