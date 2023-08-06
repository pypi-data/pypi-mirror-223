import {
  notLoggedInValidator,
  hasPersonValidator,
} from "aleksis.core/routeValidators";

export default {
  meta: {
    inMenu: true,
    titleKey: "paweljong.events.menu_title",
    icon: "mdi-calendar-text",
    validators: [hasPersonValidator],
    permission: "paweljong.view_menu",
  },
  children: [
    {
      path: "event/:slug/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.editEventBySlug",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/:slug/terms/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.viewEventTermsBySlug",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/:slug/register/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.registerEventBySlug",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "group_persons/:pk/add/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.addPersonsToGroup",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/:slug/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.eventByName",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/:slug/detail/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.eventDetailByName",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/:slug/checkpoint/",
      component: () => import("./components/event/Checkpoint.vue"),
      name: "paweljong.eventByNameCheckpoint",
    },
    {
      path: "event/:slug/start/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.registerEventBySlugStart",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "misc/set_email_needed/:slug/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.setEmailNeeded",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "misc/set_email_needed/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.setEmailNeededNoSlug",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "account/register/start/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.registerAccountStart",
      meta: {
        inMenu: true,
        titleKey: "paweljong.register.menu_title",
        icon: "mdi-account-check-outline",
        validators: [notLoggedInValidator],
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "account/register/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.registerAccount",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "events/feed/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.upcomingEventsRssFeed",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "events/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.createEvent",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "events/manage/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.manageEvents",
      meta: {
        inMenu: true,
        titleKey: "paweljong.events.manage_events.menu_title",
        icon: "mdi-calendar-edit",
        permission: "paweljong.change_events_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "vouchers/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.createVouchers",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "vouchers/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.deleteVoucherByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "vouchers/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.editVoucherByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "vouchers/:pk/print/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.printVoucherByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "vouchers/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.vouchers",
      meta: {
        inMenu: true,
        titleKey: "paweljong.events.vouchers.menu_title",
        icon: "mdi-ticket-confirmation-outline",
        permission: "paweljong.view_vouchers_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/lists/generate/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.generateLists",
      meta: {
        inMenu: true,
        titleKey: "paweljong.events.generate_lists.menu_title",
        icon: "mdi-format-list-numbered",
        permission: "paweljong.generate_lists_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/:pk/check_in/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.checkInRegistrationByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/:pk/pay/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.payRegistrationByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/:pk/retract/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.retractRegistrationByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/:pk/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.registrationByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.editRegistrationByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.deleteRegistrationByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/:pk/notification/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.registrationNotificationByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/terms/list/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.terms",
      meta: {
        inMenu: true,
        titleKey: "paweljong.events.terms.menu_title",
        icon: "mdi-gavel",
        permission: "paweljong.view_terms_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/terms/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.createTerm",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/terms/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.editTermByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/states/list/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.registrationStates",
      meta: {
        inMenu: true,
        titleKey: "paweljong.events.registration_states.menu_title",
        icon: "mdi-list-status",
        permission: "paweljong.view_registration_states_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/states/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.createRegistrationState",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "event/registrations/states/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.editRegistrationStateByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "info_mailings/list/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.infoMailings",
      meta: {
        inMenu: true,
        titleKey: "paweljong.events.info_mailings.menu_title",
        icon: "mdi-email-alert-outline",
        permission: "paweljong.view_info_mailings_rule",
      },
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "info_mailings/create/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.createInfoMailing",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "info_mailings/:pk/edit/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.editInfoMailingByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "info_mailings/:pk/delete/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "paweljong.deleteInfoMailingByPk",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
  ],
};
