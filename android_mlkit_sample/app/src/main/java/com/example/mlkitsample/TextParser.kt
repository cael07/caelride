package com.example.mlkitsample

data class CRResult(
    val plate: String = "",
    val brand: String = "",
    val color: String = "",
    val year: String = "",
    val owner: String = "",
)

object TextParser {
    private val KNOWN_BRANDS = listOf("HONDA","YAMAHA","SUZUKI","KAWASAKI","TOYOTA","NISSAN","ISUZU","MITSUBISHI","MAZDA","HYUNDAI","KIA","FORD","CHEVROLET","HINO")
    private val KNOWN_COLORS = listOf("BLACK","WHITE","RED","BLUE","GREEN","YELLOW","BROWN","SILVER","GRAY","GREY","ORANGE","GOLD","MAROON","BEIGE")

    fun parseCR(raw: String): CRResult {
        val linesRaw = raw.split('\n').map { it.trim() }
        val upperLines = linesRaw.map { it.uppercase() }
        val rawUpper = raw.uppercase()

        fun extractField(labels: List<String>, rejectGeneric: Boolean = false): String {
            val genericTokens = Regex("\\b(VEHICLE|MOTOR|TYPE|CATEGORY|WITHOUT|SIDE|CAR|FUEL|ENGINE|CHASSIS|FILE|MODEL|YEAR|MAKE|BRAND|OWNER|REGISTERED|CERTIFICATE|REGISTRATION|OFFICIAL|DEPARTMENT|TRANSPORTATION)\\b", RegexOption.IGNORE_CASE)
            val upperLabels = labels.map { it.uppercase() }
            for (i in upperLines.indices) {
                val upper = upperLines[i]
                for (label in upperLabels) {
                    val idx = upper.indexOf(label)
                    if (idx >= 0) {
                        var value = linesRaw[i].substring(idx + label.length).trim()
                        value = value.replace("^[.:\\-\\s]+".toRegex(), "").trim()
                        if (value.isNotEmpty() && upperLabels.none { value.uppercase().contains(it) }) {
                            if (!rejectGeneric || !genericTokens.containsMatchIn(value)) return value
                        }
                        val next = if (i + 1 < linesRaw.size) linesRaw[i + 1].trim() else ""
                        if (next.isNotEmpty() && upperLabels.none { next.uppercase().contains(it) }) {
                            if (!rejectGeneric || !genericTokens.containsMatchIn(next)) return next
                        }
                    }
                }
            }
            return ""
        }

        // Plate
        val plateRaw = extractField(listOf("PLATE NO","PLATE NO.","PLATE NUMBER","PLATE"), true)
        var plate = ""
        if (plateRaw.isNotBlank()) {
            val normalized = plateRaw.uppercase().replace("[^A-Z0-9]".toRegex(), " ")
            val candidates = Regex("\\b([A-Z]{1,3}\\d{2,4}[A-Z]{0,3})\\b").findAll(normalized).map { it.groupValues[1] }.toList()
            plate = if (candidates.isNotEmpty()) candidates.first() else normalized.replace("\\s+".toRegex(), "")
        }

        // Brand
        val brandRaw = extractField(listOf("MAKE/BRAND","MAKE","BRAND"), true)
        val brandCand = brandRaw.uppercase().replace("[^A-Z\\s]".toRegex(), "").trim()
        val knownBrand = KNOWN_BRANDS.firstOrNull { rawUpper.contains(it) } ?: KNOWN_BRANDS.firstOrNull { brandCand.contains(it) }
        val brand = knownBrand ?: brandCand

        // Color
        val colorRaw = extractField(listOf("COLOR"), true)
        val colorCand = colorRaw.uppercase().replace("[^A-Z\\s]".toRegex(), "").trim()
        val knownColor = KNOWN_COLORS.firstOrNull { rawUpper.contains(it) } ?: KNOWN_COLORS.firstOrNull { colorCand.contains(it) }
        val color = knownColor ?: (colorCand.split("\\s+".toRegex()).firstOrNull() ?: "")

        // Year (search for 19xx or 20xx)
        var year = ""
        val yearMatch = Regex("\\b(19|20)\\d{2}\\b").find(raw)
        if (yearMatch != null) year = yearMatch.value

        // Owner
        var owner = extractField(listOf("OWNER'S NAME","OWNERS NAME","OWNER NAME","REGISTERED OWNER"), false)
        if (owner.isBlank() || owner.split(Regex("\\s+")).size < 2 || owner.length < 8) {
            val ownerIndex = upperLines.indexOfFirst { it.contains("OWNER") }
            if (ownerIndex >= 0) {
                for (j in ownerIndex + 1 until (ownerIndex + 4).coerceAtMost(linesRaw.size)) {
                    val candidate = linesRaw[j].trim()
                    if (candidate.length > 10 && candidate.contains(' ') && !Regex("\\b(MOTOR|VEHICLE|TYPE|FUEL|MODEL|YEAR|MAKE|BRAND|ENGINE|CHASSIS|FILE|REGISTRATION|CERTIFICATE|OFFICIAL|DEPARTMENT|TRANSPORTATION)\\b", RegexOption.IGNORE_CASE).containsMatchIn(candidate)) {
                        owner = candidate
                        break
                    }
                }
            }
        }
        if (owner.isBlank()) {
            owner = linesRaw.filter { it.length > 10 && it.contains(' ') && !Regex("\\b(MOTOR|VEHICLE|TYPE|FUEL|MODEL|YEAR|MAKE|BRAND|ENGINE|CHASSIS|FILE|REGISTRATION|CERTIFICATE|OFFICIAL|DEPARTMENT|TRANSPORTATION)\\b", RegexOption.IGNORE_CASE).containsMatchIn(it) }
                .sortedByDescending { it.length }
                .firstOrNull() ?: ""
        }

        return CRResult(
            plate = plate,
            brand = brand,
            color = color,
            year = year,
            owner = owner.replace(Regex("[^A-Z\\s\\.,]", RegexOption.IGNORE_CASE), " ").replace(Regex("\\s+"), " ").trim()
        )
    }
}
