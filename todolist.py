from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def print_tasks(rows, deadlines=False):
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for number, thing in enumerate(rows):
            print(f'{number + 1}. {thing}', end='.')
            if deadlines:
                print('', thing.deadline.day, thing.deadline.strftime('%b'), end='')
            print()


def implement_menu(session):
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    case = int(input())
    while case:
        if case == 1:
            rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
            current = datetime.today()
            print(f"Today:{current.day} {current.strftime('%b')}:")
            print_tasks(rows)
        elif case == 2:
            deadline = Table.deadline
            day = 0
            while day != 8:
                current = datetime.today() + timedelta(days=day)
                print(current.strftime("%A"),
                      current.day,
                      current.strftime('%b'),
                      end=':\n'
                      )
                rows = session.query(Table) \
                    .filter(deadline == datetime.today().date() + timedelta(days=day)).all()
                print_tasks(rows)
                print()
                day += 1

        elif case == 3:
            print('All tasks:')
            rows = session.query(Table).order_by(Table.deadline).all()
            print_tasks(rows, True)
        elif case == 4:
            print('Missed tasks:')
            rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
            if len(rows) == 0:
                print('Nothing is missed!')
            else:
                print_tasks(rows)
                print('\nend')
        elif case == 5:
            print('Enter task')
            new_task = input()
            print('Enter deadline')
            deadline = input()
            new_row = Table(task=new_task,
                            deadline=datetime.strptime(deadline, '%Y-%m-%d'))
            session.add(new_row)
            session.commit()
            print('The task has been added!')

        elif case == 6:
            print('Choose the number of the task you want to delete:')
            rows = session.query(Table).order_by(Table.deadline).all()

            number = int(input())
            session.delete(rows[number - 1])
            session.commit()
            print('The task has been deleted!')
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        case = int(input())
    print('Bye!')


def main():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    implement_menu(session)


if __name__ == '__main__':
    main()
