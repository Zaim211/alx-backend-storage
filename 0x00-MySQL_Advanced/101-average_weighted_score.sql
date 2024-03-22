-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	UPDATE users
	SET average_score = (SELECT SUM(projects.weight * corrections.score) / SUM(projects.weight)
	FROM corrections
	JOIN projects
	ON projects.id = corrections.project_id
	where corrections.user_id = users.id);
END; $$
DELIMITER;
