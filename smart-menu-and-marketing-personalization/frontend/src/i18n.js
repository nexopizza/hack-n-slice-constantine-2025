import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  en: {
    translation: {
      welcome: "Welcome",
      hi: "Hi, {{name}}!",
      signOut: "Sign out",
      loginIntro: "Log in to view your account, orders and rewards.",
      username: "Username",
      password: "Password",
      usernamePlaceholder: "Choose a username",
      passwordPlaceholder: "Enter password",
      loginBtn: "Login",
      signupBtn: "Sign up",
      questionnaireTitle: "We'd like to know more about you",
      questionnairePrompt: "Would you like to do a short questionnaire?",
      yes: "Yes",
      remindLater: "Remind me later",
      languageLabel: "Language:",
      menuTitle: "Our Menu",
      menuSubtitle: "Choose your favorite",
      loadingMenu: "Loading menu...",
      loadingSub: "Fetching fresh items for you",
      loadErrorTitle: "Could not load menu",
      loadErrorSub: "Check your connection or try again.",
      retry: "Retry",
      done: "Done"
    }
  },
  fr: {
    translation: {
      welcome: "Bienvenue",
      hi: "Salut, {{name}} !",
      signOut: "Se déconnecter",
      loginIntro: "Connectez-vous pour voir votre compte, commandes et récompenses.",
      username: "Nom d'utilisateur",
      password: "Mot de passe",
      usernamePlaceholder: "Choisissez un nom d'utilisateur",
      passwordPlaceholder: "Entrez le mot de passe",
      loginBtn: "Connexion",
      signupBtn: "S'inscrire",
      questionnaireTitle: "Nous aimerions en savoir plus sur vous",
      questionnairePrompt: "Souhaitez‑vous faire un court questionnaire ?",
      yes: "Oui",
      remindLater: "Me le rappeler plus tard",
      languageLabel: "Langue :",
      menuTitle: "Notre Menu",
      menuSubtitle: "Choisissez votre favori",
      loadingMenu: "Chargement du menu…",
      loadingSub: "Récupération des éléments",
      loadErrorTitle: "Impossible de charger le menu",
      loadErrorSub: "Vérifiez votre connexion ou réessayez.",
      retry: "Réessayer",
      done: "Terminé"
    }
  },
  ar: {
    translation: {
      welcome: "مرحبًا",
      hi: "مرحبًا، {{name}}!",
      signOut: "تسجيل الخروج",
      loginIntro: "سجل الدخول لعرض حسابك، طلباتك والمكافآت.",
      username: "اسم المستخدم",
      password: "كلمة المرور",
      usernamePlaceholder: "اختر اسم مستخدم",
      passwordPlaceholder: "أدخل كلمة المرور",
      loginBtn: "تسجيل الدخول",
      signupBtn: "إنشاء حساب",
      questionnaireTitle: "نود أن نعرف المزيد عنك",
      questionnairePrompt: "هل تود إجراء استبيان قصير؟",
      yes: "نعم",
      remindLater: "ذكرني لاحقًا",
      languageLabel: "اللغة:",
      menuTitle: "قائمتنا",
      menuSubtitle: "اختر المفضلات",
      loadingMenu: "جارٍ تحميل القائمة…",
      loadingSub: "جلب العناصر",
      loadErrorTitle: "تعذّر تحميل القائمة",
      loadErrorSub: "تحقق من الاتصال أو حاول مرة أخرى.",
      retry: "إعادة المحاولة",
      done: "إنهاء"
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: localStorage.getItem("sm_lang") || "en",
  fallbackLng: "en",
  interpolation: { escapeValue: false }
});

export default i18n;
