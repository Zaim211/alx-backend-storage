-- SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

SELECT band_name AS band_name, (IFNULL(split, '2022') - formed) AS lifespan
	FROM metal_bands
	WHERE band_name = 'Glam rock'
	GROUP BY band_name
	ORDER BY lifespan DESC;
