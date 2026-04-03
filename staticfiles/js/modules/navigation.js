/**
 * Navigation Module
 * Navbar, dropdowns, and menu management
 */

/**
 * Dropdown Manager Class
 */
class DropdownManager {
  constructor(dropdownSelector) {
    this.dropdown = typeof dropdownSelector === 'string' 
      ? document.querySelector(dropdownSelector) 
      : dropdownSelector;
    
    if (!this.dropdown) {
      console.warn('Dropdown not found:', dropdownSelector);
      return;
    }

    this.trigger = this.dropdown.querySelector('[data-dropdown-trigger]');
    this.menu = this.dropdown.querySelector('[data-dropdown-menu]');
    this.isOpen = false;
    
    this.init();
  }

  /**
   * Initialize dropdown
   */
  init() {
    if (!this.trigger || !this.menu) return;

    // Click trigger to toggle
    this.trigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.toggle();
    });

    // Click outside to close
    document.addEventListener('click', (e) => {
      if (!this.dropdown.contains(e.target) && this.isOpen) {
        this.close();
      }
    });

    // Close on ESC
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.close();
      }
    });

    // Click menu items to close
    this.menu.querySelectorAll('a, button').forEach(item => {
      item.addEventListener('click', () => this.close());
    });
  }

  /**
   * Open dropdown
   */
  open() {
    this.isOpen = true;
    this.menu.classList.add('dropdown-open');
    this.trigger.setAttribute('aria-expanded', 'true');
    
    Utils?.dispatchEvent('dropdown:opened', { dropdownId: this.dropdown.id });
  }

  /**
   * Close dropdown
   */
  close() {
    this.isOpen = false;
    this.menu.classList.remove('dropdown-open');
    this.trigger.setAttribute('aria-expanded', 'false');
    
    Utils?.dispatchEvent('dropdown:closed', { dropdownId: this.dropdown.id });
  }

  /**
   * Toggle dropdown
   */
  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }
}

/**
 * Navbar Manager Class
 */
class NavbarManager {
  constructor(navbarSelector) {
    this.navbar = typeof navbarSelector === 'string' 
      ? document.querySelector(navbarSelector) 
      : navbarSelector;
    
    if (!this.navbar) {
      console.warn('Navbar not found:', navbarSelector);
      return;
    }

    this.mobileMenuBtn = this.navbar.querySelector('[data-mobile-menu-toggle]');
    this.mobileMenu = this.navbar.querySelector('[data-mobile-menu]');
    this.mobileMenuOpen = false;
    
    this.init();
  }

  /**
   * Initialize navbar
   */
  init() {
    if (!this.mobileMenuBtn) return;

    // Toggle mobile menu
    this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileMenu());

    // Close menu on link click
    this.mobileMenu?.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => this.closeMobileMenu());
    });

    // Initialize all dropdowns in navbar
    this.navbar.querySelectorAll('[data-dropdown]').forEach(dropdown => {
      new DropdownManager(dropdown);
    });

    // Close menu on resize to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 768 && this.mobileMenuOpen) {
        this.closeMobileMenu();
      }
    });
  }

  /**
   * Toggle mobile menu
   */
  toggleMobileMenu() {
    if (this.mobileMenuOpen) {
      this.closeMobileMenu();
    } else {
      this.openMobileMenu();
    }
  }

  /**
   * Open mobile menu
   */
  openMobileMenu() {
    this.mobileMenuOpen = true;
    this.mobileMenu?.classList.add('mobile-menu-open');
    this.mobileMenuBtn.setAttribute('aria-expanded', 'true');
    
    Utils?.dispatchEvent('navbar:mobile-menu-opened');
  }

  /**
   * Close mobile menu
   */
  closeMobileMenu() {
    this.mobileMenuOpen = false;
    this.mobileMenu?.classList.remove('mobile-menu-open');
    this.mobileMenuBtn.setAttribute('aria-expanded', 'false');
    
    Utils?.dispatchEvent('navbar:mobile-menu-closed');
  }

  /**
   * Set active link
   */
  setActiveLink(pathname) {
    this.navbar.querySelectorAll('a').forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === pathname) {
        link.classList.add('active');
      }
    });
  }

  /**
   * Set active by current URL
   */
  setActiveLinkByUrl() {
    const pathname = window.location.pathname;
    this.setActiveLink(pathname);
  }
}

/**
 * Tabs Manager Class
 */
class TabsManager {
  constructor(tabsContainerSelector) {
    this.container = typeof tabsContainerSelector === 'string' 
      ? document.querySelector(tabsContainerSelector) 
      : tabsContainerSelector;
    
    if (!this.container) {
      console.warn('Tabs container not found:', tabsContainerSelector);
      return;
    }

    this.tabs = Array.from(this.container.querySelectorAll('[data-tab-trigger]'));
    this.panels = Array.from(this.container.querySelectorAll('[data-tab-panel]'));
    this.activeTab = null;
    
    this.init();
  }

  /**
   * Initialize tabs
   */
  init() {
    this.tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => this.activate(index));
      
      // Set first as active by default
      if (index === 0) {
        this.activate(0);
      }
    });
  }

  /**
   * Activate tab by index
   */
  activate(index) {
    if (index < 0 || index >= this.tabs.length) return;

    // Deactivate all
    this.tabs.forEach(tab => tab.classList.remove('tab-active'));
    this.panels.forEach(panel => panel.classList.add('hidden'));

    // Activate selected
    const tab = this.tabs[index];
    const panelId = tab.dataset.tabTrigger;
    const panel = this.container.querySelector(`[data-tab-panel="${panelId}"]`);

    if (tab) tab.classList.add('tab-active');
    if (panel) panel.classList.remove('hidden');

    this.activeTab = index;
    
    Utils?.dispatchEvent('tabs:activated', { 
      tabIndex: index, 
      tabId: panelId 
    });
  }

  /**
   * Get active tab index
   */
  getActiveTab() {
    return this.activeTab;
  }
}

/**
 * Initialize all navigation elements on page
 */
function initNavigation() {
  // Initialize navbars
  document.querySelectorAll('[data-navbar]').forEach(navbar => {
    new NavbarManager(navbar);
  });

  // Initialize dropdowns
  document.querySelectorAll('[data-dropdown]').forEach(dropdown => {
    new DropdownManager(dropdown);
  });

  // Initialize tabs
  document.querySelectorAll('[data-tabs]').forEach(tabs => {
    new TabsManager(tabs);
  });

  Utils?.dispatchEvent('navigation:initialized');
}

/**
 * Export
 */
const Navigation = {
  DropdownManager,
  NavbarManager,
  TabsManager,
  initNavigation,
};

// Make available globally
window.Navigation = Navigation;
window.DropdownManager = DropdownManager;
window.NavbarManager = NavbarManager;
window.TabsManager = TabsManager;
window.initNavigation = initNavigation;

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
});

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Navigation;
}
