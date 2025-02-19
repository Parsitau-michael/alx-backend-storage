--  SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students.
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	UPDATE users u
	SET u.average_score = (
		SELECT IFNULL(SUM(c.score * p.weight) / NULLIF(SUM(p.weight), 0), 0)
	        FROM corrections c
        	JOIN projects p ON c.project_id = p.id
	        WHERE c.user_id = u.id
	    );
END $$

DELIMITER ;
