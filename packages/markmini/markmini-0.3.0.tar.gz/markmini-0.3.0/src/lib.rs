use ::markmini::Markmini as _Markmini;
use ::markmini::User;
use itertools::izip;
use pyo3::prelude::*;

#[pyclass]
pub struct Markmini {
    internal: _Markmini,
}

#[pymethods]
impl Markmini {
    #[new]
    pub fn new() -> Self {
        return Self {
            internal: _Markmini::new(),
        };
    }

    pub fn compile(&self, input: &str) -> String {
        return self.internal.compile(input);
    }

    pub fn compile_comment(&self, input: &str) -> String {
        return self.internal.compile_comment(input);
    }

    pub fn add_users(
        &mut self,
        usernames: Vec<String>,
        user_ids: Vec<String>,
        links: Vec<String>,
        fullnames: Vec<String>,
    ) {
        let mut users = Vec::with_capacity(usernames.len());
        for (username, user_id, link, fullname) in izip!(usernames, user_ids, links, fullnames) {
            users.push(User {
                username,
                user_id,
                link,
                fullname,
            });
        }
        self.internal.add_users(users);
    }
}

// This function is the entrypoint to the python module
#[pymodule]
fn markmini_py(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Markmini>()?;
    return Ok(());
}
