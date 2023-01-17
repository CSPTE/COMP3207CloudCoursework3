function getCookie(name) {
	const value = "; " + document.cookie;
	const parts = value.split("; " + name + "=");
	if (parts.length === 2) return decodeURI(parts.pop().split(";").shift()).replace("%2C", ",");
  }

function snake_to_natural(txt) {
	return txt.split("_").map((e) => {return e.substring(0, 1).toUpperCase() + e.slice(1)}).join(" ")
}

function natural_to_snake(txt) {
	return txt.toLowerCase().replaceAll(" ", "_")
}

function snake_to_natural_2(txt) {
	try {
		return txt.split("-").map((e) => {return e.substring(0, 1).toUpperCase() + e.slice(1)}).join(" ")
	} catch (e) {return ""}
}

function natural_to_snake_2(txt) {
	return txt.toLowerCase().replaceAll(" ", "-")
}

module.exports = { getCookie, snake_to_natural, natural_to_snake, snake_to_natural_2, natural_to_snake_2 }
