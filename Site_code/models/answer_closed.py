from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, DDL, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class ClosedAnswer(SQLBase):
    __tablename__ = 'answers_closed'

    id = Column(Integer, primary_key=True)

    closed_question_option_id = Column(Integer, ForeignKey("questions_closed_options.id"))
    closed_question_option = relationship("ClosedQuestionOption", back_populates="closed_answers")

    answer_id = Column(Integer, ForeignKey("answers.id"))
    answer = relationship("Answer", back_populates="closed_answers")


@event.listens_for(ClosedAnswer.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    connection.execute(
        """ CREATE OR REPLACE FUNCTION max_Ans() 
            RETURNS TRIGGER as $$
            DECLARE my_cursorGen refcursor;
            DECLARE my_cursorIn refcursor;
            DECLARE idQ integer;
            DECLARE idA integer;
            DECLARE numAns integer;
            DECLARE diffNumAns integer;
            BEGIN
                OPEN my_cursorGen FOR (SELECT DISTINCT n.answer_id
                                       FROM new AS n);
                FETCH NEXT FROM my_cursorGen INTO idA;  
                WHILE FOUND LOOP
                   OPEN my_cursorIn FOR (SELECT DISTINCT qco.closed_question_id
                                        FROM new AS n
                                        INNER JOIN questions_closed_options AS qco ON qco.id = n.closed_question_option_id);
                   FETCH NEXT FROM my_cursorIn INTO idQ;
                   WHILE FOUND LOOP
                        numAns = (SELECT COUNT(*) FROM answers_closed WHERE closed_question_option_id = idQ AND answer_id = idA);
                        diffNumAns = (SELECT COUNT(*) FROM new WHERE closed_question_option_id = idQ AND answer_id = idA);
                        IF TG_OP = 'DELETE' THEN
                            diffNumAns = -diffNumAns;
                        END IF;
                        
                        IF ((numAns+diffNumAns) > (SELECT q.max_n_of_answer 
                                    FROM questions_closed AS q 
                                    INNER JOIN questions_closed_option AS qc ON q.id=qc.closed_question_id
                                    WHERE qc.id = idQ)
                           OR numAns<(SELECT q.min_n_of_answer
                                       FROM questions_closed AS q
                                       INNER JOIN questions_closed_option AS qc ON q.id=qc.closed_question_id
                                       WHERE qc.id = idQ)) THEN
                               CLOSE my_cursorIn;
                               CLOSE my_cursorGen;
                               RETURN NULL;
                        END IF;
                        FETCH NEXT FROM my_cursorIn INTO idQ;
                   END LOOP;
                   CLOSE my_cursorIn;
                   FETCH NEXT FROM my_cursorGen INTO idA;  
                END LOOP;   
                CLOSE my_cursorGen;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql""")

    connection.execute(
        """DROP TRIGGER IF EXISTS MaxClosedAns ON answers_closed;
        CREATE TRIGGER MaxClosedAns
        BEFORE INSERT OR DELETE ON answers_closed 
        REFERENCING OLD TABLE AS old, NEW TABLE AS new
        FOR EACH STATEMENT 
        EXECUTE PROCEDURE max_Ans();"""
    )

# event.listen(ClosedAnswer, 'before_insert', trigger_maxAns)