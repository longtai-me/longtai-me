# Maintenance Guide for config.js

## Editing config.js for Content Updates
To edit content in your project, make sure to locate the `config.js` file in your main directory. Here, you can directly modify text for various sections of your site:

- **Site Title:** Change the `siteTitle` variable to update your site’s name.
- **Description:** Update the `siteDescription` variable for SEO purposes.

## File Structure
Your project consists of several key folders:

- `assets/`: Contains images, CSS, and JavaScript files.
- `pages/`: Where all your page files are located.
- `components/`: Individual parts of your site, like header, footer, etc.

## Customization Options for Themes
In the `config.js`, you'll find theme options that you can customize:

- **Theme Color:** Adjust the `themeColor` variable for your site’s primary color.
- **Font Styles:** Update the `fontFamily` variable to change your site’s typography.

## Adding New Pages
To add a new page:
1. Create a new file in the `pages/` directory, e.g., `new-page.js`.
2. Add the new page name to the `pages` array in the `config.js` file.

## Social Media Links
To update your social media links:
- Find the `socialMedia` object in the `config.js` and replace the URLs with your personal links.

## FAQ
For common questions and troubleshooting tips:
- **How do I change the site logo?** Simply replace the logo file in the `assets/` folder and update its path in `config.js`.
- **Can I add an iframe?** Yes! Just include your iframe code in the correct page file within the `pages/` directory.

If you encounter any issues, refer to our documentation or contact support.