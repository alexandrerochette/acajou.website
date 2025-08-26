

function switch_color_scheme(name) {
    /* var link = document.createElement("link");
     link.href = name + ".colorscheme.style.css";
     link.type = "text/css";
     link.rel = "stylesheet";
     link.media = "screen,print";
 
     document.getElementsByTagName("head")[0].appendChild(link);
     */

    const themeVariables = ["hero-background", "hero-text", "content-background", "content-text"]
    const computedStyles = window.getComputedStyle(document.documentElement);
    themeVariables.forEach(function (variableName) {
        console.log(variableName);
        setColorPropertyVariant(computedStyles, variableName, name)
    });


}

function setColorPropertyVariant(computedStyles, propertyBaseName, variantName) {
    const propertyVariantName = `--${variantName}-${propertyBaseName}`
    const propertyName = `--${propertyBaseName}`

    const value = computedStyles.getPropertyValue(propertyVariantName);

    document.documentElement.style.setProperty(propertyName, value);
}