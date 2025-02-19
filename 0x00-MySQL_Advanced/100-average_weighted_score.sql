-- A script that creates a stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student.
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE total_weighted_score FLOAT;
	DECLARE total_weight FLOAT;
	DECLARE computed_average FLOAT;

	SELECT SUM(c.score * p.weight), SUM(p.weight)
       	INTO total_weighted_score,  total_weight
	FROM corrections c
	JOIN projects p ON c.project_id = p.id
	WHERE c.user_id = user_id;

	IF total_weight > 0 THEN
		SET computed_average = (total_weighted_score/total_weight);
	ELSE
		SET computed_average = 0;
	END IF;

	UPDATE users
	SET average_score = computed_average
	WHERE users.id = user_id;
END $$

DELIMITER ;
