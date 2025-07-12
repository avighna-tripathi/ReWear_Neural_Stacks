```js
ReWear – Community Clothing Exchange 
Overview: 
    Develop ReWear, a web-based platform that enables users to exchange unused clothing 
    through direct swaps or a point-based redemption system. The goal is to promote sustainable 
    fashion and reduce textile waste by encouraging users to reuse wearable garments instead of 
    discarding them. 
Features: 
    User Authentication 
    Email/password signup and login 
Landing Page 
    Platform introduction 
    Calls-to-action: “Start Swapping”, “Browse Items”, “List an Item” 
    Featured items carousel 
User Dashboard 
    Profile details and points balance 
    Uploaded items overview 
    Ongoing and completed swaps list 
Item Detail Page 
    Image gallery and full item description 
    Uploader info 
    Options: “Swap Request” or “Redeem via Points” 
    Item availability status 
Add New Item Page 
    Upload images 
    Enter title, description, category, type, size, condition, and tags 
    Submit to list item 
Admin Role 
    Moderate and approve/reject item listings 
    Remove inappropriate or spam items 
    Lightweight admin panel for oversight 
```

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from 'eslint-plugin-react'

export default tseslint.config({
  // Set the react version
  settings: { react: { version: '18.3' } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```
