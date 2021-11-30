export const user = {
  namespaced: true,
  state: {
    jwt: null,
    user: null
  },
  actions: {
    async login ({ commit }, credentials) {
      try {
        const resp = await fetch(`${import.meta.env.VITE_APP_BACKEND}/auth/token/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(credentials)
        })
        if (!resp.ok) {
          console.log(`${resp.status}: ${resp.data}`)
        }
        const data = await resp.json()
        commit('login', data.token)
      }
      catch (err) {
        console.error(err)
      }
    },
    logout ({ commit }) {
      commit('logout');
    }
  },
  mutations: {
    login (state, jwt) {
      state.jwt = jwt;
      // state.user = user;
    },
    logout (state) {
      state.jwt = null;
      // state.user = null;
    }
  },
  getters: {
    isLoggedIn (state) {
      return state.jwt !== null
    }
  }
}