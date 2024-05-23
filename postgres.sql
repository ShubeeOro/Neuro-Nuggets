CREATE TABLE question (
  id SERIAL PRIMARY KEY,
  question VARCHAR(200),
  correct_answer VARCHAR(200),
  incorrect_answers VARCHAR(200),
  category VARCHAR(100),
  difficulty VARCHAR(100)
);

SELECT * FROM information_schema.columns
WHERE table_name  = 'question'