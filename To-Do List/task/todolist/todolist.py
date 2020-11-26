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
        self.actions: dict = {'1': self.today_tasks, '2': self.create_task, '0': exit}

    def init_db(self) -> None:
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def create_task(self) -> None:
        task = input('Enter task:\n')
        new_row = Table(task=task)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')

    def today_tasks(self) -> None:
        tasks = self.session.query(Table).filter(Table.deadline == self.today).all()
        print(f'\nToday {datetime.today().day} {datetime.today().strftime("%b")}:')
        if not tasks:
            print('Nothing to do!')
        else:
            for i, todo in enumerate(tasks, 1):
                print(f'{i}. {todo}')

    def menu(self) -> None:
        while True:
            print()
            choice: str = input('1) Today\'s tasks\n2) Add task\n0) Exit\n>')
            if choice in self.actions:
                self.actions[choice]()
            else:
                print('Unknown option.')


if __name__ == "__main__":
    ToDo().menu()
